# -*- coding: utf-8 -*-
"""
Created on Wednesday, 4th May 2022 6:46:49 pm
===============================================================================
@filename:  dirs.py
@project:   trollbane
@purpose:   module for handling directories
===============================================================================
"""
from getpass import getuser
from pathlib import Path


def data_path() -> Path:
    """
    this method simply returns a Path object to our data folder in Google Drive

    Returns:
        Path: data folder on Google Drive
    """
    if getuser() == 'manma':
        gdrivepath = Path('G:/My Drive/')
    elif getuser() == 'mariagabrielaayala' or getuser() == 'baltierra':
        gdrivepath = Path('/Volumes/GoogleDrive/My Drive')

    return gdrivepath.joinpath('capp-30254-final-project/datasets')
