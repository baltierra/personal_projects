import json
import math
import requests


def GetAARR(targetYear, baseLineYear, targetValue, baseLineValue):
    if targetYear == baseLineYear or baseLineValue == 0:
        return None
    else:
        valueRatio = baseLineValue / targetValue
        t = targetYear - baseLineYear
        return (math.log(valueRatio) / t)


def GetCAGR(targetYear, baseLineYear, targetValue, baseLineValue):
    if targetYear == baseLineYear or baseLineValue == 0:
        return None
    else:
        valueRatio = targetValue / baseLineValue
        power = 1 / (targetYear - baseLineYear)
        return ((valueRatio ** power) - 1)


def GetYearsAndValues(data, baselineYear):
    finalYearObj = data[len(data) - 1]
    years = []
    for d in data:
        if d['year'] < baselineYear + 1:
            years.append(d)
    if len(years) == 0:
        baseYear = data[0]['year']
        baseValue = data[0]['value']
    else:
        baseYear = years[len(years) - 1]['year']
        baseValue = years[len(years) - 1]['value']
    return {
        'baseYear': baseYear,
        'baseValue': baseValue,
        'finalYear': finalYearObj['year'],
        'finalValue': finalYearObj['value'],
    }


def GetCurrentLevel(tsData):
    if 'methodology' in tsData.keys():
        methodology = tsData['methodology']
        if(tsData['methodology']['trendMethodology'] == 'Binary'):
            return None
        values = tsData['values']
        yearsAndValues = GetYearsAndValues(
            values, tsData['methodology']['baselineYear'])
        if yearsAndValues['finalYear'] <= yearsAndValues['baseYear']:
            return None
        if methodology['trendMethodology'] == 'Likert':
            if methodology['targetValue'] - yearsAndValues['finalValue'] == 0:
                return "Target met or almost met"
            if methodology['targetValue'] - yearsAndValues['finalValue'] == 1:
                return "Close to Target"
            if methodology['targetValue'] - yearsAndValues['finalValue'] == 2:
                return "Moderate distance to target"
            if methodology['targetValue'] - yearsAndValues['finalValue'] == 3:
                return "Far from target"
            return "Very far from target"
        if 'currentLevelThresholds' in methodology.keys():
            if len(methodology['currentLevelThresholdsName']) == 5:
                if methodology['trendMethodology'] == 'CAGRR' or methodology['trendMethodology'] == 'CAGRA' or methodology['trendMethodology'] == 'AARRR' or methodology['trendMethodology'] == 'CAGRR+AARRR':
                    if methodology['normativeDirection'] == 'decrease' or methodology['normativeDirection'] == 'not increase':
                        if yearsAndValues['finalValue'] <= methodology['currentLevelThresholds'][0]:
                            return methodology['currentLevelThresholdsName'][0]
                        if yearsAndValues['finalValue'] <= methodology['currentLevelThresholds'][1]:
                            return methodology['currentLevelThresholdsName'][1]
                        if yearsAndValues['finalValue'] <= methodology['currentLevelThresholds'][2]:
                            return methodology['currentLevelThresholdsName'][2]
                        if yearsAndValues['finalValue'] <= methodology['currentLevelThresholds'][3]:
                            return methodology['currentLevelThresholdsName'][3]
                        return methodology['currentLevelThresholdsName'][4]
                    if methodology['normativeDirection'] == 'increase' or methodology['normativeDirection'] == 'not decrease':
                        if yearsAndValues['finalValue'] > methodology['currentLevelThresholds'][0]:
                            return methodology['currentLevelThresholdsName'][0]
                        if yearsAndValues['finalValue'] > methodology['currentLevelThresholds'][1]:
                            return methodology['currentLevelThresholdsName'][1]
                        if yearsAndValues['finalValue'] > methodology['currentLevelThresholds'][2]:
                            return methodology['currentLevelThresholdsName'][2]
                        if yearsAndValues['finalValue'] > methodology['currentLevelThresholds'][3]:
                            return methodology['currentLevelThresholdsName'][3]
                        return methodology['currentLevelThresholdsName'][4]
                if methodology['trendMethodology'] == 'SpecialGINI':
                    if yearsAndValues['finalValue'] <= methodology['currentLevelThresholds'][0]:
                        return methodology['currentLevelThresholdsName'][0]
                    if yearsAndValues['finalValue'] <= methodology['currentLevelThresholds'][1]:
                        return methodology['currentLevelThresholdsName'][1]
                    if yearsAndValues['finalValue'] <= methodology['currentLevelThresholds'][2]:
                        return methodology['currentLevelThresholdsName'][2]
                    if yearsAndValues['finalValue'] <= methodology['currentLevelThresholds'][3]:
                        return methodology['currentLevelThresholdsName'][3]
                    return methodology['currentLevelThresholdsName'][4]
            else:
                if yearsAndValues['finalValue'] > methodology['currentLevelThresholds'][0]:
                    return methodology['currentLevelThresholdsName'][0]
                if yearsAndValues['finalValue'] > methodology['currentLevelThresholds'][1]:
                    return methodology['currentLevelThresholdsName'][1]
                return methodology['currentLevelThresholdsName'][2]
        else:
            return None
    else:
        return None


def GetStatus(yearsAndValues, values, methodology):
    if methodology['trendMethodology'] == 'CAGRR':
        if 'targetValue' in methodology.keys():
            if methodology['normativeDirection'] == 'decrease':
                if yearsAndValues['finalValue'] == 0:
                    return 'Target Achieved'
                if methodology['targetValue'] / yearsAndValues['finalValue'] > 0.9995:
                    return 'Target Achieved'
            if methodology['normativeDirection'] == 'increase':
                if yearsAndValues['finalValue'] / methodology['targetValue'] > 0.9995:
                    return 'Target Achieved'
            if methodology['normativeDirection'] == 'decrease':
                if (yearsAndValues['baseValue'] <= methodology['targetValue']) and (yearsAndValues['baseValue'] < yearsAndValues['finalValue']):
                    return 'Deterioration'
            if methodology['normativeDirection'] == 'increase':
                if (yearsAndValues['baseValue'] >= methodology['targetValue']) and (yearsAndValues['baseValue'] > yearsAndValues['finalValue']):
                    return 'Deterioration'
        CAGRA = GetCAGR(yearsAndValues['finalYear'], yearsAndValues['baseYear'],
                        yearsAndValues['finalValue'], yearsAndValues['baseValue'])
        if 'CAGRRequire' in methodology.keys():
            CAGRT = methodology['CAGRRequire']
        else:
            CAGRT = GetCAGR(2030, yearsAndValues['baseYear'],
                            methodology['targetValue'], yearsAndValues['baseValue'])
        if CAGRA == None or CAGRT == None:
            return 'Insufficient Data'
        if CAGRT == 0:
            if methodology['normativeDirection'] == 'decrease':
                if (yearsAndValues['finalValue'] <= yearsAndValues['baseValue']):
                    return 'Target Achieved'
                else:
                    return 'Deterioration'
            if methodology['normativeDirection'] == 'increase':
                if (yearsAndValues['finalValue'] >= yearsAndValues['baseValue']):
                    return 'Target Achieved'
                else:
                    return 'Deterioration'
        CR = CAGRA / CAGRT
        try:
            if CR >= 0.95:
                return 'On Track'
            if CR >= 0.5 and CR < 0.95:
                return 'Fair progress but acceleration needed'
            if CR >= -0.1 and CR < 0.5:
                return 'Limited or No Progress'
            return 'Deterioration'
        except:
            return 'Insufficient Data'
    if methodology['trendMethodology'] == 'CAGRA':
        if isinstance(yearsAndValues['finalValue'], str) is True:
            return 'Target Achieved'
        if 'targetValue' in methodology.keys():
            if methodology['normativeDirection'] == 'decrease':
                if yearsAndValues['finalValue'] == 0:
                    return 'Target Achieved'
                if methodology['targetValue'] / yearsAndValues['finalValue'] > 0.9995:
                    return 'Target Achieved'
            if methodology['normativeDirection'] == 'increase':
                if yearsAndValues['finalValue'] / methodology['targetValue'] > 0.9995:
                    return 'Target Achieved'
        CAGRA = GetCAGR(yearsAndValues['finalYear'], yearsAndValues['baseYear'],
                        yearsAndValues['finalValue'], yearsAndValues['baseValue'])
        if CAGRA == None:
            return 'Insufficient Data'
        if methodology['normativeDirection'] == 'decrease' or methodology['normativeDirection'] == 'not increase':
            try:
                if CAGRA < methodology['CAGRLimit'][2]:
                    return 'On Track'
                if CAGRA < methodology['CAGRLimit'][1] and CAGRA >= methodology['CAGRLimit'][2]:
                    return 'Fair progress but acceleration needed'
                if CAGRA > methodology['CAGRLimit'][1] and CAGRA <= methodology['CAGRLimit'][0]:
                    return 'Limited or No Progress'
                return 'Deterioration'
            except:
                return 'Insufficient Data'
        else:
            try:
                if CAGRA > methodology['CAGRLimit'][0]:
                    return 'On Track'
                if CAGRA > methodology['CAGRLimit'][1] and CAGRA <= methodology['CAGRLimit'][0]:
                    return 'Fair progress but acceleration needed'
                if CAGRA > methodology['CAGRLimit'][2] and CAGRA <= methodology['CAGRLimit'][1]:
                    return 'Limited or No Progress'
                return 'Deterioration'
            except:
                return 'Insufficient Data'
    if methodology['trendMethodology'] == 'AARRR':
        if isinstance(yearsAndValues['finalValue'], str) is True:
            return 'Target Achieved'
        if methodology['normativeDirection'] == 'decrease' or methodology['normativeDirection'] == 'not increase':
            if yearsAndValues['finalValue'] == 0:
                return 'Target Achieved'
            if methodology['targetValue'] / yearsAndValues['finalValue'] > 0.9995:
                return 'Target Achieved'
        if methodology['normativeDirection'] == 'increase' or methodology['normativeDirection'] == 'not decrease':
            if yearsAndValues['finalValue'] / methodology['targetValue'] > 0.9995:
                return 'Target Achieved'
        if methodology['normativeDirection'] == 'decrease' or methodology['normativeDirection'] == 'not increase':
            if (yearsAndValues['baseValue'] <= methodology['targetValue']) and (yearsAndValues['baseValue'] < yearsAndValues['finalValue']):
                return 'Deterioration'
        if methodology['normativeDirection'] == 'increase' or methodology['normativeDirection'] == 'not decrease':
            if (yearsAndValues['baseValue'] >= methodology['targetValue']) and (yearsAndValues['baseValue'] > yearsAndValues['finalValue']):
                return 'Deterioration'
        AARRObserved = GetAARR(yearsAndValues['finalYear'], yearsAndValues['baseYear'],
                               yearsAndValues['finalValue'], yearsAndValues['baseValue'])
        AARRRequire = GetAARR(2030, yearsAndValues['baseYear'],
                              methodology['targetValue'], yearsAndValues['baseValue'])
        if AARRObserved == None or AARRRequire == None:
            return 'Insufficient Data'
        if AARRObserved >= AARRRequire:
            return 'On Track'
        if AARRObserved >= 0.5:
            return 'Fair progress but acceleration needed'
        if AARRObserved > -0.5 and AARRObserved < 0.5:
            return 'Limited or No Progress'
        return 'Deterioration'
    if methodology['trendMethodology'] == 'CAGRR+AARRR':
        if isinstance(yearsAndValues['finalValue'], str) is True:
            return 'Target Achieved'
        if methodology['normativeDirection'] == 'decrease':
            if yearsAndValues['finalValue'] == 0:
                return 'Target Achieved'
            if methodology['targetValue'] / yearsAndValues['finalValue'] > 0.9995:
                return 'Target Achieved'
        if methodology['normativeDirection'] == 'increase':
            if yearsAndValues['finalValue'] / methodology['targetValue'] > 0.9995:
                return 'Target Achieved'
        if methodology['normativeDirection'] == 'decrease':
            if (yearsAndValues['baseValue'] <= methodology['targetValue']) and (yearsAndValues['baseValue'] < yearsAndValues['finalValue']):
                return 'Deterioration'
        if methodology['normativeDirection'] == 'increase':
            if (yearsAndValues['baseValue'] >= methodology['targetValue']) and (yearsAndValues['baseValue'] > yearsAndValues['finalValue']):
                return 'Deterioration'
        AARRObserved = GetAARR(yearsAndValues['finalYear'], yearsAndValues['baseYear'],
                               yearsAndValues['finalValue'], yearsAndValues['baseValue'])
        AARRRequire = GetAARR(2030, yearsAndValues['baseYear'],
                              methodology['targetValue'], yearsAndValues['baseValue'])
        if AARRObserved == None or AARRRequire == None:
            return 'Insufficient Data'
        if AARRRequire == 0:
            if methodology['normativeDirection'] == 'decrease':
                if (yearsAndValues['finalValue'] <= yearsAndValues['baseValue']):
                    return 'Target Achieved'
                else:
                    return 'Deterioration'
            if methodology['normativeDirection'] == 'increase':
                if (yearsAndValues['finalValue'] >= yearsAndValues['baseValue']):
                    return 'Target Achieved'
                else:
                    return 'Deterioration'
        CR = AARRObserved / AARRRequire
        try:
            if CR >= 0.95:
                return 'On Track'
            if CR >= 0.5 and CR < 0.95:
                return 'Fair progress but acceleration needed'
            if CR >= -0.1 and CR < 0.5:
                return 'Limited or No Progress'
            return 'Deterioration'
        except:
            return 'Insufficient Data'
    if methodology['trendMethodology'] == 'Binary':
        if len(values) == 0:
            return 'Insufficient Data'
        if values[len(values) - 1]['value'] == methodology['value']:
            return 'Target Achieved'
        else:
            return 'Target Not Achieved'
    if methodology['trendMethodology'] == 'Doubling':
        targetValue = yearsAndValues['baseValue'] * 2
        if yearsAndValues['finalValue'] / targetValue > 0.9995:
            return 'Target Achieved'
        CAGRA = GetCAGR(yearsAndValues['finalYear'], yearsAndValues['baseYear'],
                        yearsAndValues['finalValue'], yearsAndValues['baseValue'])
        CAGRT = GetCAGR(2030, yearsAndValues['baseYear'],
                        targetValue, yearsAndValues['baseValue'])
        if CAGRA == None or CAGRT == None:
            return 'Insufficient Data'
        CR = CAGRA / CAGRT
        try:
            if CR >= 0.95:
                return 'On Track'
            if CR >= 0.5 and CR < 0.95:
                return 'Fair progress but acceleration needed'
            if CR >= -0.1 and CR < 0.5:
                return 'Limited or No Progress'
            return 'Deterioration'
        except:
            return 'Insufficient Data'
    if methodology['trendMethodology'] == 'Halfing':
        targetValue = yearsAndValues['baseValue'] / 2
        if yearsAndValues['finalValue'] == 0:
            return 'Target Achieved'
        if targetValue / yearsAndValues['finalValue'] > 0.9995:
            return 'Target Achieved'
        CAGRA = GetCAGR(yearsAndValues['finalYear'], yearsAndValues['baseYear'],
                        yearsAndValues['finalValue'], yearsAndValues['baseValue'])
        CAGRT = GetCAGR(2030, yearsAndValues['baseYear'],
                        targetValue, yearsAndValues['baseValue'])
        if CAGRA == None or CAGRT == None:
            return 'Insufficient Data'
        CR = CAGRA / CAGRT
        try:
            if CR >= 0.95:
                return 'On Track'
            if CR >= 0.5 and CR < 0.95:
                return 'Fair progress but acceleration needed'
            if CR >= -0.1 and CR < 0.5:
                return 'Limited or No Progress'
            return 'Deterioration'
        except:
            return 'Insufficient Data'
    if methodology['trendMethodology'] == 'SpecialGINI':
        if yearsAndValues['finalValue'] == 0:
            return 'Target Achieved'
        if methodology['targetValue'] / yearsAndValues['finalValue'] > 0.9995:
            return 'Target Achieved'
        CAGRA = GetCAGR(yearsAndValues['finalYear'], yearsAndValues['baseYear'],
                        yearsAndValues['finalValue'], yearsAndValues['baseValue'])
        percentPointChange = (
            (yearsAndValues['finalValue'] - yearsAndValues['baseValue']) * 100) / yearsAndValues['finalValue']
        if CAGRA == None:
            return 'Insufficient Data'
        try:
            if CAGRA < -0.01 and percentPointChange <= -1:
                return 'On Track'
            if percentPointChange <= -1:
                return 'Fair progress but acceleration needed'
            if percentPointChange > -1 and percentPointChange < 1:
                return 'Limited or No Progress'
            return 'Deterioration'
        except:
            return 'Insufficient Data'
    if methodology['trendMethodology'] == 'Likert':
        if methodology['normativeDirection'] == 'increase':
            if (yearsAndValues['finalValue'] == methodology['targetValue']):
                return 'Target Achieved'
            if (yearsAndValues['baseYear'] == yearsAndValues['finalYear']):
                return 'Insufficient Data'
            if (yearsAndValues['finalValue'] - yearsAndValues['baseValue'] >= 2):
                return 'On Track'
            if (yearsAndValues['finalValue'] - yearsAndValues['baseValue'] == 1):
                return 'Fair progress but acceleration needed'
            if (yearsAndValues['finalValue'] - yearsAndValues['baseValue'] == 0):
                return 'Limited or No Progress'
            return 'Deterioration'
        else:
            if (yearsAndValues['finalValue'] == methodology['targetValue']):
                return 'Target Achieved'
            if (yearsAndValues['baseYear'] == yearsAndValues['finalYear']):
                return 'Insufficient Data'
            if (yearsAndValues['baseValue'] - yearsAndValues['finalValue'] >= 2):
                return 'On Track'
            if (yearsAndValues['baseValue'] - yearsAndValues['finalValue'] == 1):
                return 'Fair progress but acceleration needed'
            if (yearsAndValues['baseValue'] - yearsAndValues['finalValue'] == 0):
                return 'Limited or No Progress'
            return 'Deterioration'


def GetTimeSeriesStatus(tsData):
    if 'methodology' in tsData.keys():
        values = tsData['values']
        if(tsData['methodology']['trendMethodology'] == 'Binary'):
            return [GetStatus(None, values, tsData['methodology']), None, None]
        yearsAndValues = GetYearsAndValues(
            values, tsData['methodology']['baselineYear'])
        if (yearsAndValues['finalYear'] <= 2015):
            return ['No Data After 2015', None, None]
        return [GetStatus(yearsAndValues, values, tsData['methodology']), yearsAndValues['baseYear'], yearsAndValues['finalYear']]
    else:
        return ['Methodology Unavailable', None, None]


def GetIndicatorStatus(tsDataWithStatus, indicator):
    tsForIndicators = []
    for d in tsDataWithStatus:
        if d['indicator'] == indicator:
            if 'status' in d.keys():
                if d['status'] != 'Insufficient Data' and d['status'] != 'No Data After 2015' and d['status'] != None and d['status'] != 'Methodology Unavailable':
                    tsForIndicators.append(d)
    i = 0
    for d in tsForIndicators:
        if d['status'] == 'Target Achieved' or d['status'] == 'On Track':
            i = i + 1
        if d['status'] == 'Fair progress but acceleration needed' or d['status'] == 'Target Not Achieved':
            i = i + 2
        if d['status'] == 'Limited or No Progress':
            i = i + 3
        if d['status'] == 'Deterioration':
            i = i + 4
    if i == 0:
        return None
    else:
        if (i / len(tsForIndicators)) < 1.5:
            return 'On Track'
        if (i / len(tsForIndicators)) >= 1.5 and (i / len(tsForIndicators)) <= 2.5:
            return 'For Review'
        if (i / len(tsForIndicators)) > 2.5:
            return 'Identified Gap'


def GetTargetStatus(indicatorsWithStatus, target):
    indicatorsForTargets = []
    for d in indicatorsWithStatus:
        if d['target'] == target:
            if 'status' in d.keys():
                if d['status'] != 'Insufficient Data' and d['status'] != None:
                    indicatorsForTargets.append(d)
    i = 0
    for d in indicatorsForTargets:
        if d['status'] == 'Target Achieved' or d['status'] == 'On Track':
            i = i + 1
        if d['status'] == 'For Review':
            i = i + 2
        if d['status'] == 'Identified Gap':
            i = i + 3
    if i == 0:
        return None
    else:
        if (i / len(indicatorsForTargets)) < 1.5:
            return 'On Track'
        if (i / len(indicatorsForTargets)) >= 1.5 and (i / len(indicatorsForTargets)) <= 2.5:
            return 'For Review'
        if (i / len(indicatorsForTargets)) > 2.5:
            return 'Identified Gap'


def GetGoalStatus(targetssWithStatus, goal):
    indicatorsForTargets = []
    for d in targetssWithStatus:
        if d['goal'] == goal:
            if 'status' in d.keys():
                if d['status'] != 'Insufficient Data' and d['status'] != None:
                    indicatorsForTargets.append(d)
    i = 0
    for d in indicatorsForTargets:
        if d['status'] == 'Target Achieved' or d['status'] == 'On Track':
            i = i + 1
        if d['status'] == 'For Review':
            i = i + 2
        if d['status'] == 'Identified Gap':
            i = i + 3
    if i == 0:
        return None
    else:
        if (i / len(indicatorsForTargets)) < 1.5:
            return 'On Track'
        if (i / len(indicatorsForTargets)) >= 1.5 and (i / len(indicatorsForTargets)) <= 2.5:
            return 'For Review'
        if (i / len(indicatorsForTargets)) > 2.5:
            return 'Identified Gap'


# Reads URL from json file
with open("urls.json", "r") as sources:
    urls = json.load(sources)
    
url = urls["countryTaxonomy"]
country = requests.get(url)
countries = json.loads(country.text)
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

countryStatus = []

for country in countries:
    dataFile = open('./CountryDataCleaned/' +
                    country['Alpha-3 code-1'] + '.json', encoding="utf8")
    data = json.load(dataFile)
    i = 0
    tsDataWithStatus = []
    timeSeriesStatus = []
    for d in data:
        for value in d['values']:
            if isinstance(value['value'], str) is True:
                if value['value'] == 'N':
                    value['label'] = 'NA'
                    value['value'] = 0
                else:
                    value['label'] = value['value']
                    value['value'] = float(value['value'][1:])
        if 'methodology' in d.keys():
            d['currentLevelAssessment'] = GetCurrentLevel(d)
            d['status'] = GetTimeSeriesStatus(d)[0]
            d['methodology']['baseYear'] = GetTimeSeriesStatus(d)[1]
            d['methodology']['latestAvailable'] = GetTimeSeriesStatus(d)[2]
        else:
            d['status'] = 'Methodology Unavailable'
            d['currentLevelAssessment'] = None
        tsDataWithStatus.append(d)
    for d in tsDataWithStatus:
        if 'status' in d.keys():
            s = d['status']
        else:
            s = None
        if 'currentLevelAssessment' in d.keys():
            c = d['currentLevelAssessment']
        else:
            c = None
        if 'methodology' in d.keys() and d['series'] != '***':
            if d['methodology']['trendMethodology'] == 'Binary':
                isBinary = True
            else:
                isBinary = False
            timeSeriesStatus.append({
                'goal': d['goal'],
                'target': d['target'],
                'indicator': d['indicator'],
                'seriesDescription': d['seriesDescription'],
                'baseYear': d['methodology']['baseYear'],
                'latestYear': d['methodology']['latestAvailable'],
                'isBinary': isBinary,
                'status': s,
                'currentLevelAssessment': c
            })
    indicatorList = []
    targetList = []
    goalList = []
    for d in tsDataWithStatus:
        if d['indicator'] not in indicatorList:
            indicatorList.append(d['indicator'])
        if d['target'] not in targetList:
            targetList.append(d['target'])
        if d['goal'] not in goalList:
            goalList.append(d['goal'])
    indicatorsStatus = []
    targetsStatus = []
    goalsStatus = []
    noOfIndicatorsWithData = [0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for indicator in indicatorList:
        status = GetIndicatorStatus(tsDataWithStatus, indicator)
        if status != None:
            noOfIndicatorsWithData[int(indicator.split(
                '.')[0]) - 1] = noOfIndicatorsWithData[int(indicator.split('.')[0]) - 1] + 1
        indicatorsStatus.append({
            'goal': indicator.split('.')[0],
            'target': indicator.split('.')[0] + '.' + indicator.split('.')[1],
            'indicator': indicator,
            'status': status
        })
    for target in targetList:
        status = GetTargetStatus(indicatorsStatus, target)
        targetsStatus.append({
            'goal': target.split('.')[0],
            'target': target,
            'status': status
        })
    for goal in goalList:
        status = GetGoalStatus(targetsStatus, goal)
        goalsStatus.append({
            'goal': int(goal),
            'noOfIndicatorsWithData': noOfIndicatorsWithData[int(goal) - 1],
            'status': status
        })
    countryData = {
        'countryCode': country['Alpha-3 code-1'],
        'goalStatus': goalsStatus,
        'targetStatus': targetsStatus,
        'indicatorStatus': indicatorsStatus,
        'tsData': tsDataWithStatus
    }
    countryStatus.append({
        'countryCode': country['Alpha-3 code-1'],
        'timeSeriesStatus': timeSeriesStatus
    })
    with open('./CountryDataCleanedWithStatus/' +
              country['Alpha-3 code-1'] + '.json', 'w') as outfile:
        json.dump(countryData, outfile, indent=2)

with open('./AllCountryData.json', 'w') as outfile:
    json.dump(countryStatus, outfile, indent=2)