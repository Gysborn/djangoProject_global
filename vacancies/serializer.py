from rest_framework import serializers

from vacancies.models import *


class VacancyListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)

    class Meta:
        model = Vacancy
        fields = ['id', 'text', 'slug', 'text', 'status', 'username']


class VacancyDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(max_length=50)
    skills = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Vacancy
        fields = '__all__'


class VacancyCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    skills = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Skill.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Vacancy
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        self._skills = self.initial_data.pop('skills')
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        vacancy = Vacancy.objects.create(**validated_data)
        for skill in self._skills:
            skill_obj, _ = Skill.objects.get_or_create(name=skill)
            vacancy.skills.add(skill_obj)

        vacancy.save()
        return vacancy


class VacancyUpdateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created = serializers.DateField(read_only=True)
    skills = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Skill.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Vacancy
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        self._skills = self.initial_data.pop('skills')
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        vacancy = super().save()

        for skill in self._skills:
            skill_obj, _ = Skill.objects.get_or_create(name=skill)
            vacancy.skills.add(skill_obj)

        vacancy.save()
        return vacancy


class VacancyDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vacancy
        fields = ['id']

# class SkillsSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField(max_length=20)
#     is_active = serializers.BooleanField()s
# skills = serializers.ManyRelatedField(child_relation=i)
