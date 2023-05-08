# -*- coding: utf-8 -*-
"""
Created on Wednesday, 4th May 2022 6:43:14 pm
===============================================================================
@filename:  loader.py
@project:   trollbane
@purpose:   main module for handling loading data into memory
===============================================================================
"""
from datetime import datetime

import pandas as pd

from trollbane.paths import data_path


class DataLoader:
    def __init__(self, drive=True) -> None:
        self.datapath = data_path()
        self.today = datetime.today()
        self.allowed = {'notes', 'ratings'}
        self.drive = drive

    def load_file(self, ftype: str) -> pd.DataFrame:
        """
        Loads the latest birdwatch datafile stored in Google Drive. If no file
        is found, it downloads the latest file from the birdwatch website.
        Additionally, if the file found on Google Drive is not from the same
        date as `today`, it downloads a new file and saves it on Google Drive.

        Args:
            ftype (str): {'notes', 'ratings'}

        Returns:
            pd.DataFrame: data set fetched.
        """
        if ftype not in self.allowed:
            raise ValueError(f'ftype {ftype} not in {self.allowed}')
        todaystr = self.today.strftime('%Y%m%d')

        fpath = self.datapath.joinpath(
            'raw',
            'birdwatch',
            f'{todaystr}-{ftype}.csv')

        if fpath.exists() and self.drive:
            df = pd.read_csv(fpath)
        else:
            df = self._download_file(ftype=ftype)

        return df

    def _download_file(self, ftype: str) -> pd.DataFrame:
        """
        this method downloads a file type, either notes or ratings, from the
        birdwatch website and saves it on our google drive folder. if multiple
        the file is saved with the date of download as a prefix, which means
        that if there are multiple downloads in a day, the earlier file from
        the day will be overwritten.

        Args:
            ftype (str): {'notes', 'ratings'}

        Returns:
            pd.DataFrame: data set fetched.
        """

        if ftype not in self.allowed:
            raise ValueError(f'ftype {ftype} not in {self.allowed}')

        if ftype == 'notes':
            stub = 'notes/notes-00000.tsv'
        elif ftype == 'ratings':
            stub = 'noteRatings/ratings-00000.tsv'

        baseurl = 'https://ton.twimg.com/birdwatch-public-data'
        url = '/'.join((
            baseurl,
            self.today.strftime('%Y/%m/%d'),
            stub)
        )

        df = pd.read_csv(url, sep='\t')
        df.columns = df.columns.str.lower()

        if self.drive:
            df.to_csv(
                data_path().joinpath(
                    'raw',
                    'birdwatch',
                    f"{self.today.strftime('%Y%m%d')}-{ftype}.csv"),
                index=False)

        return df
