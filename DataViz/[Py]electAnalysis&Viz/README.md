Fabian Araneda Baltierra (baltierra)


1) project -- main directory


2) install.sh -- creates virtual env and runs necessary packages


3) requirements.txt -- package requirements for virtual environment


4) data -- contains the project's data

    4.1) data.csv -- final merged file with CDC data, election results and controls

    4.2) merge.py -- code that merges datasets

    4.3) 2020_election_results.csv -- scraped data with 2020 Presidential Election results

    4.4) fips_codes.csv -- list of FIPS codes used for merging purposes

    4.5) controls.csv -- contains downloaded controls data at county level

    4.6) abbreviations.csv -- list of state names and abbreviations for merging purposes

    4.7) cdc_api -- directory with code to extract data from CDC API and extracted data

    4.8) election_crawler -- directory with election crawler code


5) visual_exp -- contains code for data visualization map


6) regression -- contains regression code of vaccination rates on election results


7) past_deliverables -- includes deliverables 1 and 2


8) README.md -- this file
