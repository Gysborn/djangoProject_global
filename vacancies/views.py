import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from vacancies.models import *


def hello(request):
    return HttpResponse("Hello Django")


class VacancyListView(ListView):
    model = Vacancy

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        search = request.GET.get('text')
        if search:
            self.object_list = self.object_list.filter(text=search)

        return JsonResponse([{'id': vacancy.id, 'text': vacancy.text} for vacancy in self.object_list],
                            safe=False)


class VacancyDetailView(DetailView):
    model = Vacancy

    def get(self, request, *args, **kwargs):
        vacancy = self.get_object()

        return JsonResponse(
            {
                "id": vacancy.id,
                "text": vacancy.text,
                "slug": vacancy.slug,
                "user_id": vacancy.user_id,
                "status": vacancy.status,
                "created": vacancy.created,
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class VacancyCreateView(CreateView):
    model = Vacancy
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        vacancy_data = json.loads(request.body)

        vacancy = Vacancy.objects.create(**vacancy_data)
        return JsonResponse({
            'id': vacancy.id,
            'text': vacancy.text,
        })


@method_decorator(csrf_exempt, name='dispatch')
class VacancyUpdateView(UpdateView):
    model = Vacancy
    fields = ['slug', 'text', 'status', 'skills']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        vacancy_data = json.loads(request.body)
        self.object.slug = vacancy_data['slug']
        self.object.text = vacancy_data['text']
        self.object.status = vacancy_data['status']

        for skill in vacancy_data['skills']:
            try:
                skill_obj = Skill.objects.get(name=skill)
            except Skill.DoesNotExist:
                return JsonResponse({'error': 'Skill not found'}, status=404)
            self.object.skills.add(skill_obj)

        self.object.save()
        return JsonResponse({
            'id': self.object.id,
            'text': self.object.text,
            'slug': self.object.slug,
            'status': self.object.status,
            'created': self.object.created,
            'user': self.object.user_id,
            'skills': list(self.object.skills.all().values_list('name', flat=True)),
        })


@method_decorator(csrf_exempt, name='dispatch')
class VacancyDeleteView(DeleteView):
    model = Vacancy
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({
            'status': 'ok',
        }, status=200)
