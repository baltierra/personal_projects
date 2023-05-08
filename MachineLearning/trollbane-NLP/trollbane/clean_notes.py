# -*- coding: utf-8 -*-
"""
Created on Thursday, 12th May 2022 8:04:14 pm
===============================================================================
@filename:  clean_notes.py
@project:   trollbane
@purpose:   cleaning script for the notes dataset; mostly does text cleaning on
            the summaries
===============================================================================
"""
from string import punctuation

import argparse
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.data import find
from nltk.downloader import download
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from trollbane.loader import DataLoader
from trollbane.paths import data_path

try:
    find('tokenizers/punkt')
except LookupError:
    download('punkt')

try:
    find('corpora/stopwords')
except LookupError:
    download('stopwords')

try:
    find('corpora/wordnet')
except LookupError:
    download('wordnet')

try:
    find('corpora/omw-1.4')
except LookupError:
    download('omw-1.4')


def lemmatize_summary(lemmatizer: WordNetLemmatizer,
                      summary: list[str]) -> list[str]:
    return [lemmatizer.lemmatize(w) for w in summary]


def clean_text(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs light cleaning on the `summary` column in the note dataset in
    order to make the text easier to train on.

    Args:
        df (pd.DataFrame): notes dataset

    Returns:
        pd.DataFrame: the input df with the cleaned summary column
    """
    # drop all non-ascii characters
    df['summary'] = (
        df['summary']
        .str.encode(encoding='ascii', errors='ignore')
        .str.decode('ascii'))
    df['summary'] = df['summary'].str.strip()
    df = df[df['summary'] != ''].copy()

    df['summary'] = df['summary'].str.replace('&quot;', '')

    # here we get rid of all urls, but we keep a dummy whether it has one in
    # the summary
    df['has_url'] = np.where(df['summary'].str.contains('http'), 1, 0)

    df['summary'] = df['summary'].replace(r'http\S+', '', regex=True)
    df['summary'] = df['summary'].replace(r'www\S+', '', regex=True)
    # we drop the summaries that just put a URL as the summary
    df.dropna(subset='summary', inplace=True)

    df = df[~df['summary'].str.startswith('[TEST, NOT REAL]')].copy()
    df['summary'] = df['summary'].str.strip().str.lower()

    # get rid of english stopwords
    engstop = stopwords.words('english')
    pat = r'\b(?:{})\b'.format('|'.join(engstop))
    df['summary'] = df['summary'].str.replace(pat, '', regex=True)

    # remove punctuation
    df['summary'] = df['summary'].replace(
        '[{}]'.format(punctuation),
        ' ',
        regex=True)
    df['summary'] = df['summary'].str.strip()

    # tokenize
    df['summary'] = df['summary'].apply(word_tokenize)

    # lemmatize
    lemmatizer = WordNetLemmatizer()
    df['summary'] = df['summary'].apply(
        lambda x: lemmatize_summary(lemmatizer, x))
    df['summary'] = df['summary'].str.join(' ')

    # drop all comments that contain `birdwatch` as some of these are tests
    df = df[~df['summary'].str.contains('birdwatch')]

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--nodrive', action='store_true')
    args = parser.parse_args()

    if args.nodrive:
        dl = DataLoader(drive=False)
        notdf = dl.load_file('notes')
        notdf = clean_text(notdf)
        notdf.to_parquet(
            'notes-clean.parquet.gzip',
            compression='gzip',
            index=False)
    else:
        dl = DataLoader()
        notdf = dl.load_file('notes')
        notdf = clean_text(notdf)
        notdf.to_parquet(
            data_path().joinpath('clean', 'notes-clean.parquet.gzip'),
            compression='gzip',
            index=False)
