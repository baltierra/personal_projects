Repo for CAPP 30254 Final Project | Spring 2022

TEAM: capp-30254-trollbane
DATE: 6/2/2022 (project last updated)

TEAM MEMBERS:
    Fabian Araneda Baltierra (baltierra)
    Gabriela Ayala (mariagabrielaa)
    Ken Kliesner (kenkliesner)
    Manuel Martinez (manmart)
    Andrew Warfield (awarfield)



1) environment.yml -- creates virtual env and runs necessary packages


2) figs -- contains the project's figures 


3) README.md -- this file


4) setup.py -- package setup for virtual environment


5) trollbane -- main directory

    5.1) clean_notes.py -- cleaning script for the notes dataset; mostly does text cleanin on the summaries
    
    5.2) data_stats.py -- gets statistics based on the birdwatch data

    5.3) feat_engineer.py -- creates a feature that evaulates credibility of notes using ratings table

    5.4) loader.py -- main module for handling loading data into memory

    5.5) paths.py -- module for handling directories

    5.6) train_cred.py -- creates model based off of credibility ratings

    5.7) train_notes.py -- creates model based off of notes
