from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    MALE = 'm'
    FEMALE = 'f'
    SEX = [(MALE, 'Male'), (FEMALE, 'Female')]

    HR = 'hr'
    EMPLOYEE = 'employee'
    UNKNOWN = 'unknown'
    ROLE = [(HR, HR), (UNKNOWN, UNKNOWN), (EMPLOYEE, EMPLOYEE)]

    sex = models.CharField(max_length=1, choices=SEX, default=MALE)
    role = models.CharField(max_length=10, choices=ROLE, default=UNKNOWN)


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'