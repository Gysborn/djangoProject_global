import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from vacancies.models import Vacancy


def hello(request):
    return HttpResponse("Hello Django")


@csrf_exempt
def index(request):
    if request.method == 'GET':
        vacancies = Vacancy.objects.all()
        search = request.GET.get('text')
        if search:
            vacancies = vacancies.filter(text=search)

        return JsonResponse([{'id': vacancy.id, 'text': vacancy.text} for vacancy in vacancies],
                            safe=False)

    elif request.method == 'POST':
        vacancy_data = json.loads(request.body)
        vacancy = Vacancy()
        vacancy.text = vacancy_data['text']
        vacancy.save()
        return JsonResponse({'id': vacancy.id, 'text': vacancy.text},
                            safe=False)


def get(request, vacancy_id):
    if request.method == 'GET':
        try:
            vacancy = Vacancy.objects.get(pk=vacancy_id)
        except Vacancy.DoesNotExist:
            return JsonResponse({'error': 'Page not found'}, status=404)

    return JsonResponse(
        {
            "id": vacancy.id,
            "text": vacancy.text
        }
    )
