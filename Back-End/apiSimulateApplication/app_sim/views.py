from django.shortcuts import render
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from app_sim.models import WeightedCareer
from app_sim.serializers import WeightedCareerSerializer

def estimate_ranking(lang_score, math_score, grade):
    ranking = -52.84 + 1.151 * grade - 0.01571 * lang_score - 0.02076 * math_score
    if ranking > 850:
        return 850
    else:
        return ranking

def estimate_sat_scores(float):
    return 77.777778 * float + 72.222222

def calculate_nem(grade):
    nem_values = {'4.0':'162', '4.1':'185', '4.2':'209', '4.3':'233', '4.4':'257', '4.5':'280', '4.6':'304', '4.7':'328', '4.8':'352', '4.9':'375',
                  '5.0':'399', '5.1':'423', '5.2':'447', '5.3':'470', '5.4':'494', '5.5':'517', '5.6':'538', '5.7':'560', '5.8':'582', '5.9':'604',
                  '6.0':'626', '6.1':'648', '6.2':'669', '6.3':'691', '6.4':'713', '6.5':'735', '6.6':'757', '6.7':'779', '6.8':'801', '6.9':'823',
                  '7.0':'845',}
    return float(nem_values[grade])
    

@csrf_exempt
def simulationApi(request,id=0):
    if request.method=='GET':
        #Create a dictionary to store results
        results = {'application_success':'',
                   'biggest_weight':'',
                   'ranking_and_nem_over_40':''}
        
        #Get parameters from query and convert to appropriate scores where needed
        parameters = dict(request.GET)
        unique_code = parameters['career_id'][0]
        
        if float(parameters['lang'][0]) == 0:
            lang_score = 0
        else:
            lang_score = estimate_sat_scores(float(parameters['lang'][0]))
            
        if  float(parameters['math'][0]) == 0:
            math_score = 0
        else:
            math_score = estimate_sat_scores(float(parameters['math'][0]))
        
        if float(parameters['hist'][0]) == 0:
            hist_score = 0
        else:
            hist_score = estimate_sat_scores(float(parameters['hist'][0]))
            
        if float(parameters['scie'][0]) == 0:
            scie_score = 0
        else:
            scie_score = estimate_sat_scores(float(parameters['scie'][0]))
            
        #Convert gpa-like-grade into nem score
        grade = calculate_nem(parameters['grade'][0])
        
        #Estimate missing parameter based on OLS coefficients
        ranking_score = estimate_ranking(lang_score, math_score, grade)
        print(ranking_score)
        
        #Look into database for the needed record
        weighted_career = WeightedCareer.objects.filter(unique_code = unique_code)
        #End if record not found with a message
        if len(weighted_career) == 0:
            return JsonResponse({'Error':'Carrera no encontrada en la base de datos'}, safe=False)
        #Serialize data
        weighted_career_serializer = WeightedCareerSerializer(weighted_career, many=True)
        
        #Decompose record's information into needed parameters
        threshold = float(weighted_career_serializer.data[0]['weighted_threshold'])
        nem = weighted_career_serializer.data[0]['nem_weight']/100
        ranking = weighted_career_serializer.data[0]['ranking_weight']/100
        
        #Create a dictionary to store test weights
        test_weights = {}
        math = weighted_career_serializer.data[0]['math_weight']/100
        test_weights['Matemáticas'] = math
        lang = weighted_career_serializer.data[0]['lang_weight']/100
        test_weights['Lenguaje y Comunicación'] = lang
        hist = weighted_career_serializer.data[0]['hist_weight']/100
        test_weights['Historia'] = hist
        scie = weighted_career_serializer.data[0]['scie_weight']/100
        test_weights['Ciencias'] = scie
        
        #Verify condition for additional message
        if nem + ranking > 0.4:
            results['ranking_and_nem_over_40'] = '1'
            
        #Check for tests higher weights
            max_weights = [key for key, value in test_weights.items() if value == max(test_weights.values())]
            results['biggest_weight'] = max_weights
          
            
        #This answers requests from students not in high school
        if math_score == lang_score == hist_score == scie_score == 0:
            results['application_success'] = '3'
            return JsonResponse(results, safe=False)
        
          
        #This filters university careers without score requirements
        if threshold == 0:
            results['application_success'] = '2'
            return JsonResponse(results, safe=False)
        
        #Simulate application
        #There some majors where you can use either history or science special test score
        if (nem + ranking + math + lang + hist + scie) > 1 and hist == scie:
            if hist_score == 0:
                total_score = grade * nem + ranking_score * ranking + math_score * math + lang_score * lang + scie_score * scie
            elif scie_score == 0:
                total_score = grade * nem + ranking_score * ranking + math_score * math + lang_score * lang + hist_score * hist
            else:
                total_score = grade * nem + ranking_score * ranking + math_score * math + lang_score * lang + hist_score * hist
        #For all the others
        else:
            total_score = grade * nem + ranking_score * ranking + math_score * math +  lang_score * lang + hist_score * hist + scie_score * scie
        
               
        #Return result
        if total_score >= threshold: #successful application
            results['application_success'] = '1'
            return JsonResponse(results, safe=False)
        else: #failed application
            results['application_success'] = '0'
            return JsonResponse(results, safe=False)