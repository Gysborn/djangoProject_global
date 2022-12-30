import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from vacancies.models import Vacancy


def hello(request):
    return HttpResponse("Hello Django")


@method_decorator(csrf_exempt, name='dispatch')
class VacancyView(View):
    def get(self, request):
        vacancies = Vacancy.objects.all()
        search = request.GET.get('text')
        if search:
            vacancies = vacancies.filter(text=search)

        return JsonResponse([{'id': vacancy.id, 'text': vacancy.text} for vacancy in vacancies],
                            safe=False)

    def post(self, request):
        vacancy_data = json.loads(request.body)
        vacancy = Vacancy()
        vacancy.text = vacancy_data['text']
        vacancy.save()
        return JsonResponse({'id': vacancy.id, 'text': vacancy.text},
                            safe=False)


class VacancyDetailView(DetailView):
    model = Vacancy
    def get(self, request, *args, **kwargs):
        vacancy = self.get_object()


        return JsonResponse(
            {
                "id": vacancy.id,
                "text": vacancy.text
            }
        )
