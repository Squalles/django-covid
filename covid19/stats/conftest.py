import pytest
from faker import Faker

from stats.models import Country, LiveStatistic

fake = Faker()


@pytest.fixture
def countries() -> None:
    objs = [{"name": fake.country()} for _ in range(5)]
    for obj in objs:
        Country.objects.create(**obj)
    return None


@pytest.fixture
def live_statistics(countries: Country) -> list:
    objs = [{
        "new_cases": fake.random_number(),
        "new_deaths": fake.random_number(),
        "active_cases": fake.random_number(),
        "critical": fake.random_number(),
        "total_cases": fake.random_number(),
        "total_deaths": fake.random_number(),
        "total_recovered": fake.random_number(),
        "total_tests": fake.random_number(),
        "country": country
    } for country in Country.objects.all()]
    for obj in objs:
        LiveStatistic.objects.create(**obj)
    return objs
