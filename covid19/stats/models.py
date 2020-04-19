from datetime import date

from django.db import models
from django.utils import timezone


class Country(models.Model):
    name: str = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'country'
        verbose_name_plural = 'countries'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class LiveStatistic(models.Model):
    date: date = models.DateField(default=timezone.now)
    new_cases: int = models.IntegerField(blank=True, null=True)
    new_deaths: int = models.IntegerField(blank=True, null=True)
    active_cases: int = models.IntegerField(blank=True, null=True)
    critical: int = models.IntegerField(blank=True, null=True)
    total_cases: int = models.IntegerField(blank=True, null=True)
    total_deaths: int = models.IntegerField(blank=True, null=True)
    total_recovered: int = models.IntegerField(blank=True, null=True)
    total_tests: int = models.IntegerField(blank=True, null=True)
    country: Country = models.ForeignKey(Country,
                                         on_delete=models.CASCADE,
                                         related_name='live_statistics')

    class Meta:
        verbose_name = 'Live statistic'
        verbose_name_plural = 'Live statistics'

    def __str__(self) -> str:
        return '{} - {}'.format(self.country.name, self.date)
