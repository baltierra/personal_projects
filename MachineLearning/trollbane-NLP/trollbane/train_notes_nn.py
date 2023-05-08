# -*- coding: utf-8 -*-
"""
Created on Thursday, 26th May 2022 10:06:25 pm
===============================================================================
@filename:  train_notes_nn.py
@project:   trollbane
@purpose:   train a classifier for notes using neural networks
===============================================================================
"""
import time

import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from torch import nn
from torch.utils.data import DataLoader
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator

from trollbane.paths import data_path


class TextClassificationModel(nn.Module):

    def __init__(self, vocab_size, embed_dim, num_class):
        super(TextClassificationModel, self).__init__()
        self.embedding = nn.EmbeddingBag(vocab_size, embed_dim, sparse=True)
        self.fc = nn.Linear(embed_dim, num_class)
        self.init_weights()

    def init_weights(self):
        initrange = 0.5
        self.embedding.weight.data.uniform_(-initrange, initrange)
        self.fc.weight.data.uniform_(-initrange, initrange)
        self.fc.bias.data.zero_()

    def forward(self, text, offsets):
        embedded = self.embedding(text, offsets)
        return self.fc(embedded)


def yield_tokens(data_iter):
    tokenizer = get_tokenizer('basic_english')
    for _, text in data_iter:
        yield tokenizer(text)


def collate_batch(batch):
    tokenizer = get_tokenizer('basic_english')
    label_list, text_list, offsets = [], [], [0]
    for (_label, _text) in batch:
        label_list.append(_label)
        processed_text = torch.tensor(
            vocab(tokenizer(_text)),
            dtype=torch.int64)
        text_list.append(processed_text)
        offsets.append(processed_text.size(0))
    label_list = torch.tensor(label_list, dtype=torch.int64)
    offsets = torch.tensor(offsets[:-1]).cumsum(dim=0)
    text_list = torch.cat(text_list)
    return label_list.to(device), text_list.to(device), offsets.to(device)


def train(dataloader):
    model.train()
    total_acc, total_count = 0, 0
    log_interval = 50
    start_time = time.time()

    for idx, (label, text, offsets) in enumerate(dataloader):
        optimizer.zero_grad()
        predicted_label = model(text, offsets)
        loss = criterion(predicted_label, label)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 0.1)
        optimizer.step()
        total_acc += (predicted_label.argmax(1) == label).sum().item()
        total_count += label.size(0)
        if idx % log_interval == 0 and idx > 0:
            elapsed = time.time() - start_time
            print('| epoch {:3d} | {:5d}/{:5d} batches '
                  '| accuracy {:8.3f}'.format(epoch, idx, len(dataloader),
                                              total_acc/total_count))
            total_acc, total_count = 0, 0
            start_time = time.time()


def evaluate(dataloader):
    model.eval()
    total_acc, total_count = 0, 0

    with torch.no_grad():
        for idx, (label, text, offsets) in enumerate(dataloader):
            predicted_label = model(text, offsets)
            loss = criterion(predicted_label, label)
            total_acc += (predicted_label.argmax(1) == label).sum().item()
            total_count += label.size(0)
    return total_acc/total_count


if __name__ == '__main__':
    df = pd.read_parquet(
        data_path().joinpath('clean', 'notes-clean.parquet.gzip'),
        columns=['classification', 'summary'])

    y = np.where(df['classification'].str.contains('MISINFORMED'), 1, 0)

    X_train, X_test, y_train, y_test = train_test_split(
        df['summary'].tolist(), y.tolist(),
        test_size=0.2,
        random_state=42)

    train_iter = list(zip(y_train, X_train))
    test_iter = list(zip(y_test, X_test))
    vocab = build_vocab_from_iterator(
        yield_tokens(list(zip(y, df['summary']))),
        specials=['<unk>'])

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    trainloader: DataLoader = DataLoader(
        train_iter,
        batch_size=64,
        shuffle=True,
        collate_fn=collate_batch)
    testloader: DataLoader = DataLoader(
        test_iter,
        batch_size=64,
        shuffle=True,
        collate_fn=collate_batch)

    num_class = len(set([label for (label, _) in train_iter]))
    vocab_size = len(vocab)
    emsize = 64
    model = TextClassificationModel(vocab_size, emsize, num_class).to(device)

    EPOCHS = 10  # epoch
    LR = 10  # learning rate

    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=LR)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, 1, gamma=0.1)
    total_accu = None

    for epoch in range(1, EPOCHS + 1):
        epoch_start_time = time.time()
        train(trainloader)
        accu_val = evaluate(testloader)
        if total_accu is not None and total_accu > accu_val:
            scheduler.step()
        else:
            total_accu = accu_val
        print('-' * 59)
        print('| end of epoch {:3d} | time: {:5.2f}s | '
              'valid accuracy {:8.3f} '.format(
                  epoch,
                  time.time() - epoch_start_time,
                  accu_val))
        print('-' * 59)
