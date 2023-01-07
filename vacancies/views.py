import json

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.http import HttpResponse, JsonResponse
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

        self.object_list = self.object_list.select_related('user').prefetch_related('skills').order_by('text')
        # Метод сортировки выбранному полю (text) методом order_by
        # select_related (работает только для ForeignKey)помогает сформировать join по модели User
        # что бы сокр. кол. запросов


        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        vacancies = [{'id': vacancy.id, 'text': vacancy.text,
                      'skills': list(map(str, vacancy.skills.all()))} for vacancy in page_obj]
        result = {
            'items': vacancies,
            'num_pages': paginator.num_pages,
            'total': paginator.count,
        }

        return JsonResponse(result, safe=False)


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
                "skills": [skill.name for skill in vacancy.skills.all()],
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class VacancyCreateView(CreateView):
    model = Vacancy
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        vacancy_data = json.loads(request.body)

        vacancy = Vacancy.objects.create(**vacancy_data)

        for skill in vacancy_data['skills']:
            skill_obj, created = Skill.objects.get_or_create(
                name=skill,
                defaults={
                    'is_active': True
                }
            )
            vacancy.skills.add(skill_obj)
        vacancy.save()

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


class UserVacancyDetailView(View):
    def get(self, request):
        qs = User.objects.annotate(vacancies=Count('vacancy'))
        # Применяем annotate к объекту User считаем кол. вакансий встроенным методом Count

        paginator = Paginator(qs, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users = [{'id': i.id, 'name': i.username, 'vacancies': i.vacancies} for i in page_obj]

        response = {
            'items': users,
            'total': paginator.count,
            'num_pages': paginator.num_pages,
            'avg': qs.aggregate(avg=Avg('vacancies'))['avg']
            #Терминальная функция aggregate применяется ко всем записям сразу
            #В данном случае посчитали среднее кол. объявлений на пользователя
        }

        return JsonResponse(response)