#!/bin/bash

# Run first Python script: gather and format data
python3 /Users/fabs/Documents/_CODING/undp_2023/CountryData/generationScript/etl/formatData.py

# Run second Python script: clean data
python3 /Users/fabs/Documents/_CODING/undp_2023/CountryData/generationScript/etl/countryDataCleanUp.py

# Run third Python script: update data with status
python3 /Users/fabs/Documents/_CODING/undp_2023/CountryData/generationScript/etl/getCountryStatus.py
