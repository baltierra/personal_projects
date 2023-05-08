# -*- coding: utf-8 -*-
"""
Created on Saturday, 14th May 2022 9:59:38 pm
===============================================================================
@filename:  feat_engineer.py
@project:   trollbane
@purpose:   creates a feature that evaulates credibility of notes using ratings
            table
===============================================================================
"""

import argparse
import numpy as np
import pandas as pd

from trollbane.loader import DataLoader
from trollbane.paths import data_path

if __name__ == "__main__":
    """
    The goal here is to engineer a feature that includes all of the information about
    how credible a note is. Current approach is to transform all of the columns preceeded with
    'not' to -1,0 so that when we sum() the rows of the dataframe it results in a lower credibility
    rating for less helpful notes. This collapses all of the ratings for a note into one value.
    Choose not to normalize credibility by number of ratings; maybe this changes in the future.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('--nodrive', action='store_true')
    args = parser.parse_args()

    if args.nodrive:
        dl = DataLoader(drive=False)
        ratings = dl.load_file('ratings')
    else:
        dl = DataLoader()
        ratings = dl.load_file('ratings')

    ratings.drop(['createdatmillis', 'version', 'participantid'], axis = 1,  inplace=True)
    ratings.set_index('noteid', inplace=True)

    for col in ratings.loc[:, ratings.columns.str.contains('not')]:
        ratings[col].where(ratings[col] == 0, -1, inplace=True)

    ratings['helpfulnesslevel'].replace('SOMEWHAT_HELPFUL', 0, inplace=True)
    ratings['helpfulnesslevel'].replace('HELPFUL', 1, inplace=True)
    ratings['helpfulnesslevel'].replace('NOT_HELPFUL', -1, inplace=True)

    ratings['cred'] = ratings.sum(axis=1)
    ratings.reset_index(inplace=True)

    engineered = ratings.groupby(['noteid']).sum().reset_index()
    engineered = engineered[['cred', 'noteid']]

    notes = pd.read_parquet(
    'notes-clean.parquet.gzip')
    df = notes.merge(engineered, on='noteid')

    df.to_parquet(
        'notes-clean.parquet.gzip',
        compression='gzip',
        index=False)
