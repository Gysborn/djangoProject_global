from django.contrib import admin
from django.urls import path

from vacancies import views
from vacancies.views import *

urlpatterns = [
    path('', VacancyListView.as_view()),
    path('<int:pk>/', VacancyDetailView.as_view()),
    path('create/', VacancyCreateView.as_view()),
    path('update/<int:pk>/', VacancyUpdateView.as_view()),
    path('delete/<int:pk>/', VacancyDeleteView.as_view()),

]