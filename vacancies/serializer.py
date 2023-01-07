from rest_framework import serializers

from vacancies.models import *


class VacancySerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    class Meta:
        model = Vacancy
        fields = ['id', 'text', 'slug', 'text', 'status', 'username']


class VacancyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'

# class SkillsSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField(max_length=20)
#     is_active = serializers.BooleanField()s
    # skills = serializers.ManyRelatedField(child_relation=i)
