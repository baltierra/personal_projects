import requests
import json
import copy

# Open json file with external urls and load into local variables
with open("urls.json", "r") as sources:
    urls = json.load(sources)
urlTaxonomy = urls["countryTaxonomy"]
urlStats = urls["undpStats"]

# Fetch countries
country = requests.get(urlTaxonomy)

for j in range(0, 1):
    print(j)
    countryFromTaxonomy = json.loads(country.text)[j]
    res = requests.get(urlStats + countryFromTaxonomy['Numeric code']+'&page=1&pageSize=1000')
    response = json.loads(res.text)
    dataTemp = response['data']

    for page in range(2, response['totalPages'] + 1):
        res = requests.get(urlStats + countryFromTaxonomy['Numeric code']+'&page=' + str(page) + '&pageSize=1000')
        response = json.loads(res.text)
        dataTemp = dataTemp + response['data']
    indicatorSplitData = []
    dataFormatted = []
    attributeSeries = []
    dataSeries = []

    for row in dataTemp:
        for indicator in row['indicator']:
            dataCopy = copy.deepcopy(row)
            dataCopy['indicator'] = indicator
            dataCopy['goal'] = indicator.split('.')[0]
            dataCopy['target'] = indicator.split(
                '.')[0] + '.' + indicator.split('.')[1]
            indicatorSplitData.append(dataCopy)

    for row in indicatorSplitData:
        attr = row['dimensions']
        attr['series'] = row['series']
        attr['goal'] = row['goal']
        attr['target'] = row['target']
        attr['indicator'] = row['indicator']
        attr1 = copy.deepcopy(attr)
        attr1['seriesDescription'] = row['seriesDescription']
        attr1['values'] = []
        if attr not in attributeSeries:
            attributeSeries.append(attr)
            dataSeries.append(attr1)
        index = attributeSeries.index(attr)
        try:
            if row['value'] == 'NaN':
                val = None
            else:
                val = float(row['value'])
            dataSeries[index]['values'].append({
                'year': row['timePeriodStart'],
                'value': val
            })
        except:
            if row['value'][0] == '>' or row['value'][0] == '<':
                dataSeries[index]['values'].append({
                    'year': row['timePeriodStart'],
                    'value': row['value']
                })

    with open('targets.json', encoding="utf8") as targets_file:
        targets = json.load(targets_file)
        indicatorList = [t['indicator'] for t in targets]

    for d in dataSeries:
        indicator = d['indicator']
        try:
            index = indicatorList.index(indicator)
            d['targets'] = {
                'targetValue': targets[index]['targetValue'],
                'type': targets[index]['type'],
            }
        except:
            d['targets'] = None

    #Backup folder
    with open('countryDataList/' + countryFromTaxonomy['Alpha-3 code-1'] + '.json', 'w') as outfile:
        json.dump(dataSeries, outfile, indent=2)
    
    #Folder to be used for the Cleaning up script
    with open('TimeSeriesData/' + countryFromTaxonomy['Alpha-3 code-1'] + '.json', 'w') as outfile:
        json.dump(dataSeries, outfile, indent=2)