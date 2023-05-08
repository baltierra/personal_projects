@echo off

REM Run first Python script: gather and format data
python C:\Users\fabs\Documents\_CODING\undp_2023\CountryData\generationScript\etl\formatData.py

REM Run second Python script: clean data
REM python C:\Users\fabs\Documents\_CODING\undp_2023\CountryData\generationScript\etl\countryDataCleanUp.py

REM Run third Python script: update data with status
python C:\Users\fabs\Documents\_CODING\undp_2023\CountryData\generationScript\etl\getCountryStatus.py
