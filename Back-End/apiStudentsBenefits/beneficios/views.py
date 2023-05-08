import requests

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from beneficios.models import GovBenefits
from beneficios.serializers import BenefitsSerializer

def auth_token(email, password):
    body = {'captcha': 'Este es el código secreto', 'username': email, 'password': password}
    response = requests.post("https://api.consiliumbots.com/dfm/dfm/api/token/", data=body)
    json = response.json()
    return json['access']


def get_answer(student_id, token, question):
    return requests.get(f"https://api.consiliumbots.com/dfm/dfm/studentanswernew?question__id={question}&student__user__identifier={student_id}", headers={'Authorization': token})


EMAIL = 'fabianaraneda@consiliumbots.com'
PASSWORD = '#n55a@WGy*8k4NK!KwD!DBJ5TRO86*'

# Create your views here.
@csrf_exempt
def benefitsApi(request,id=0):
    if request.method=='GET':
        benefits = GovBenefits.objects.all()
        benefits_serializer=BenefitsSerializer(benefits,many=True)
        return JsonResponse(benefits_serializer.data,safe=False)

def personalized_benefits(request, rut='22200184-6'):
    print('RUT: '+ request.GET.get('rut', ''))
    if request.method=='GET' and rut:
        token = auth_token(EMAIL, PASSWORD)
        answer_168, answer_172, answer_173, answer_368 = -1, -1, -1, -1
        
        if get_answer(rut, token, 168).json():
            answer_168 = get_answer(rut, token, 168).json()[0]
            
        if get_answer(rut, token, 172).json():
            answer_172 = get_answer(rut, token, 172).json()[0]
        
        if get_answer(rut, token, 173).json():
            answer_173 = get_answer(rut, token, 173).json()[0]
        
        if get_answer(rut, token, 368).json():
            answer_368 = get_answer(rut, token, 368).json()[0]
              
        if (answer_172 != -1 and answer_173 != -1 and answer_168 != -1) and \
        (answer_172['answer'] == 0 and answer_173['answer'] == 0 and answer_168['answer'] == 4):
            benefits = GovBenefits.objects.filter(ben_id__in = {1, 4})
            benefits_serializer=BenefitsSerializer(benefits,many=True)
            return JsonResponse(benefits_serializer.data,safe=False)
        elif answer_168 != -1 and (answer_168['answer'] == 2 or answer_168['answer'] == 3):
            benefits = GovBenefits.objects.filter(ben_id__in = {2, 3})
            benefits_serializer=BenefitsSerializer(benefits,many=True)
            return JsonResponse(benefits_serializer.data,safe=False)
        elif answer_368 != -1 and answer_368['answer'] == 6:
            benefits = GovBenefits.objects.filter(ben_id = 6)
            benefits_serializer=BenefitsSerializer(benefits,many=True)
            return JsonResponse(benefits_serializer.data,safe=False)
        else:
            benefits = GovBenefits.objects.filter(ben_id__in = {1, 2, 5})
            benefits_serializer=BenefitsSerializer(benefits,many=True)
            return JsonResponse(benefits_serializer.data,safe=False)

    

