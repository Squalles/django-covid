import json
import math
from itertools import islice
from operator import itemgetter
from typing import Optional, Union

import pandas as pd
import requests
from django.utils import timezone

from stats.models import Country, LiveStatistic


class DataStore:
    batch_size = 100

    def __init__(self, data: str):
        self.data = json.loads(data)

    @staticmethod
    def diff(first: list, second: list) -> list:
        second = set(second)
        return [item for item in first if item not in second]

    def create_countries(self) -> None:
        existing_countries = list(
            Country.objects.values_list('name', flat=True))
        countries = [dct['country'] for dct in self.data]
        to_add = self.diff(countries, existing_countries)
        country_objs = (Country(name=obj['country']) for obj in self.data
                        if obj['country'] in to_add)
        while True:
            batch = list(islice(country_objs, self.batch_size))
            if not batch:
                break
            Country.objects.bulk_create(batch, self.batch_size)

    def create_live_statistics(self) -> None:
        today = timezone.now()
        countries = Country.objects.values_list('id', flat=True)
        for dct, country_id in zip(self.data, countries):
            dct['country_id'] = country_id
            dct.pop('country')
        if not LiveStatistic.objects.filter(date=today).exists():
            objs = (LiveStatistic(**obj) for obj in self.data)
            while True:
                batch = list(islice(objs, self.batch_size))
                if not batch:
                    break
                LiveStatistic.objects.bulk_create(batch, self.batch_size)
        else:
            objs = LiveStatistic.objects.filter(date=today)
            for dct, obj in zip(self.data, objs):
                if obj.id == dct['country_id']:
                    obj.new_cases = dct['new_cases']
                    obj.new_deaths = dct['new_deaths']
                    obj.active_cases = dct['active_cases']
                    obj.critical = dct['critical']
                    obj.total_cases = dct['total_cases']
                    obj.total_deaths = dct['total_deaths']
                    obj.total_recovered = dct['total_recovered']
                    obj.total_tests = dct['total_tests']
            fields = ('new_cases', 'new_deaths', 'active_cases', 'critical',
                      'total_cases', 'total_deaths', 'total_recovered',
                      'total_tests')
            LiveStatistic.objects.bulk_update(objs, fields, self.batch_size)

    def save(self) -> None:
        self.create_countries()
        self.create_live_statistics()


class TableScraper:
    url = 'https://www.worldometers.info/coronavirus/#countries'
    fields_mapper = {
        'Country,Other': 'country',
        'TotalCases': 'total_cases',
        'NewCases': 'new_cases',
        'TotalDeaths': 'total_deaths',
        'NewDeaths': 'new_deaths',
        'TotalRecovered': 'total_recovered',
        'ActiveCases': 'active_cases',
        'Serious,Critical': 'critical',
        'TotalTests': 'total_tests'
    }

    def __init__(self) -> None:
        self.store = DataStore

    @staticmethod
    def get_value(
            value: Union[str, int, float]) -> Optional[Union[str, int, float]]:
        if isinstance(value, str):
            if value.startswith('+'):
                return int(value.replace(',', ''))
            return value
        elif math.isnan(value):
            return None
        else:
            return value

    def build_data(self, df: pd.DataFrame) -> str:
        res = list()
        for idx, row in df.iterrows():
            c = row['Country,Other']
            if c == 'World' or c == 'Total:':
                continue
            data = {
                self.fields_mapper[k]: self.get_value(v)
                for (k, v) in row.items() if k in self.fields_mapper
            }
            res.append(data)
        res = sorted(res, key=itemgetter('country'), reverse=False)
        res = json.dumps(res, ensure_ascii=False)
        return res

    def scrap(self) -> None:
        resp = requests.get(self.url)
        resp.raise_for_status()
        df = pd.read_html(resp.text)[0]
        res = self.build_data(df)
        store = self.store(data=res)
        store.save()
