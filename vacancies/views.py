import json

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from vacancies.models import *
from vacancies.permissions import VacancyCreatePermission
from vacancies.serializer import *


def hello(request):
    return HttpResponse("Hello Django")


class SkillsViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class VacancyListView(ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer

    # def get(self, request, *args, **kwargs):
    #     super().get(request, *args, **kwargs)
    #
    #     search = request.GET.get('text')
    #     if search:
    #         self.object_list = self.object_list.filter(text=search)
    #
    #     self.object_list = self.object_list.select_related('user').prefetch_related('skills').order_by('text')
    # Метод сортировки выбранному полю (text) методом order_by
    # select_related (работает только для ForeignKey)помогает сформировать join по модели User
    # что бы сокр. кол. запросов

    # paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)
    #
    # list(map(lambda x: setattr(x, 'username', x.user.username if x.user else None), page_obj))
    # for ob in page_obj:
    #     # setattr(ob, "skills", [ob.name for ob in ob.skills.all()])
    #     return JsonResponse([ob.name for ob in ob.skills.all()], safe=False)

    # vacancies = [{'id': vacancy.id, 'text': vacancy.text,
    #               'skills': list(map(str, vacancy.skills.all()))} for vacancy in page_obj]
    # result = {
    #     'items': VacancyListSerializer(page_obj, many=True).data,
    #     'num_pages': paginator.num_pages,
    #     'total': paginator.count,
    # }
    #
    # return JsonResponse(result, safe=False)


class VacancyDetailView(RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer
    permission_classes = [IsAuthenticated]


class VacancyCreateView(CreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyCreateSerializer
    permission_classes = [IsAuthenticated, VacancyCreatePermission]


class VacancyUpdateView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer


class VacancyDeleteView(DestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDeleteSerializer

    # model = Vacancy
    # success_url = '/'
    #
    # def delete(self, request, *args, **kwargs):
    #     super().delete(request, *args, **kwargs)
    #
    #     return JsonResponse({
    #         'status': 'ok',
    #     }, status=200)


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
            # Терминальная функция aggregate применяется ко всем записям сразу
            # В данном случае посчитали среднее кол. объявлений на пользователя
        }

        return JsonResponse(response)
