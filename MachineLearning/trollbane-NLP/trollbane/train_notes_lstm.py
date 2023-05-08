# -*- coding: utf-8 -*-
"""
Created on Wednesday, 1st June 2022 20:35:17 pm
===============================================================================
@filename:  train_notes_lstm.py
@project:   trollbane
@purpose:   Implement ltsm model with pytorch
===============================================================================
"""

import argparse
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from keras.callbacks import EarlyStopping
from keras import backend as K
from sklearn.model_selection import train_test_split
import seaborn as sns
from keras.preprocessing.text import Tokenizer
from trollbane.paths import data_path


if __name__ == "__main__":

    def recall_m(y_test, y_pred):
        true_positives = K.sum(K.round(K.clip(y_test * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_test, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall


    parser = argparse.ArgumentParser()
    parser.add_argument('--nodrive', action='store_true')
    args = parser.parse_args()

    #====================== CREATING DATA FRAME ======================#
    if args.nodrive:
        df = pd.read_parquet(
            'notes-clean.parquet.gzip',
            columns=['classification', 'summary'])
    else:
        df = pd.read_parquet(
            data_path().joinpath('clean', 'notes-clean.parquet.gzip'),
            columns=['classification', 'summary'])
    #====================== CREATING DATA FRAME ======================#
 

    #======================== PREPARING DATA ========================#
    X = np.array(df['summary'])
    y = np.where(df['classification'].str.contains('MISINFORMED'), 1, 0)

    # The maximum number of words to be used. (most frequent)
    MAX_NB_WORDS = 15000
    # Max number of words in each note.
    MAX_SEQUENCE_LENGTH = 250
    # This is fixed.
    EMBEDDING_DIM = 32

    tokenizer = Tokenizer(num_words=MAX_NB_WORDS,
                        filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)
    tokenizer.fit_on_texts(df['summary'].values)
    X = tokenizer.texts_to_sequences(df['summary'].values)
    X = tf.keras.utils.pad_sequences(X, maxlen=MAX_SEQUENCE_LENGTH)
    y = pd.get_dummies(df['classification']).values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42)
    #======================== PREPARING DATA ========================#


    #======================== CREATE MODEL AND TRAIN  ========================#
    model = Sequential()
    model.add(Embedding(MAX_NB_WORDS, EMBEDDING_DIM, input_length=X.shape[1]))
    model.add(SpatialDropout1D(0.2))
    model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(2, activation='sigmoid'))
    model.compile(loss='binary_crossentropy',
                optimizer='adam',
                metrics=['accuracy', recall_m])

    epochs = 5
    batch_size = 32

    history = model.fit(X_train,
                        y_train,
                        epochs=epochs,
                        batch_size=batch_size,
                        validation_split=0.1,
                        callbacks=[EarlyStopping(monitor='val_loss',
                                                patience=3,
                                                min_delta=0.0001)])
    #======================== CREATE MODEL AND TRAIN  ========================#


    #======================= EVALUATE MODEL AND GRAPH  =======================#
    y_pred = model.predict(X_test)

    accr = model.evaluate(X_test,y_test)
    print('Test set\n  Loss: {:0.3f}\n  Accuracy: {:0.3f}\n  Recall: {:0.3f}'.format(accr[0], accr[1], accr[2]))


    plt.title('Loss')
    plt.plot(history.history['loss'], label='train')
    plt.plot(history.history['val_loss'], label='test')
    plt.legend()
    plt.show()

    plt.title('Accuracy')
    plt.plot(history.history['accuracy'], label='train')
    plt.plot(history.history['val_accuracy'], label='test')
    plt.legend()
    plt.show()
    #======================= EVALUATE MODEL AND GRAPH  =======================#
