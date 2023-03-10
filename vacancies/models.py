from django.db import models
from django.db.models import CASCADE

from authentication.models import User


class Skill(models.Model):
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    STATUS = [
        ('draft', 'черновик'),
        ('open', 'Открыто'),
        ('closed', 'Закрыто'),
    ]

    slug = models.SlugField(max_length=50)
    text = models.CharField(max_length=2000)
    status = models.CharField(max_length=6, choices=STATUS, default='draft')
    created = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=CASCADE, null=True)
    skills = models.ManyToManyField(Skill)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        #ordering = ['text', ...]  # Сортировка через таблицу по умолчанию (только через список[]) глобальный метод
        #привязывается ко всем запросам

    def __str__(self):
        return self.slug

    @property
    def username(self):
        return self.user.username if self.user else None

