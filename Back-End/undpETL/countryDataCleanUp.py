import json
import copy
import requests

def read_json_file(file_path):
    with open(file_path, encoding="utf8") as file:
        return json.load(file)

def get_country_data(url):
    response = requests.get(url)
    return json.loads(response.text)

def clean_data(data, tsToUse, methodologies, country_code):
    cleaned_data = []

    for d in data:
        d = {k: v for k, v in d.items() if k not in ['targets', 'trendMethodology']}
        tsToCompare = copy.deepcopy(d)

        unique_values = [val for i, val in enumerate(d['values']) if val not in d['values'][i + 1:] and val['value'] is not None]
        d['values'] = sorted(unique_values, key=lambda x: x['year'])

        tsToCompare.pop('values', None)
        if tsToCompare in tsToUse or tsToCompare['series'] == '***':
            if d['values']:
                for methodology in methodologies:
                    if (methodology['series'] == d['series'] or tsToCompare['series'] == '***') and methodology['indicator'] == d['indicator']:
                        methodology_to_add = copy.deepcopy(methodology)
                        baseline_year = methodology['baselineYear']['all']
                        if country_code in methodology['baselineYear']:
                            baseline_year = methodology['baselineYear'][country_code]

                        methodology_to_add = {k: v for k, v in methodology_to_add.items() if k not in ['series', 'indicator', 'baselineYear']}
                        d['methodology'] = methodology_to_add
                        if methodology_to_add['trendMethodology'] != 'Binary':
                            d['methodology']['baselineYear'] = baseline_year

                cleaned_data.append(d)

    return cleaned_data

def write_json_file(data, file_path):
    with open(file_path, 'w') as outfile:
        json.dump(data, outfile, indent=2)

methodologies = read_json_file('methodology.json')

# Open json file with external urls and load into local variable
with open("urls.json", "r") as sources:
    urls = json.load(sources)
url = urls["countryTaxonomy"]
countries = get_country_data(url)
# This code is to test for just one country, comment the line above and uncomment code below
# countries = [{'Alpha-3 code-1': 'AFG',
#              'Country or Area': 'Afghanistan',
#              'Alpha-2 code': 'AF', 'Numeric code': '4',
#              'Latitude (average)': '33.0',
#              'Longitude (average)': '65.0',
#              'Group 1': 'Asia',
#              'Group 2': 'Southern Asia',
#              'Group 3': '',
#              'LDC': True,
#              'LLDC': True,
#              'SIDS': False,
#              'Development classification': 'LDC, LLDC',
#              'Income group': 'Low income'}]

for country in countries:
    country_code = country['Alpha-3 code-1']
    tsToUse = read_json_file(f'./tsToUse/{country_code}.json')
    data = read_json_file(f'./TimeSeriesData/{country_code}.json')

    country_data_cleaned = clean_data(data, tsToUse, methodologies, country_code)
    write_json_file(country_data_cleaned, f'./CountryDataCleaned/{country_code}.json')
