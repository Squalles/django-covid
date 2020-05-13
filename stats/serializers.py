import datetime

from rest_framework import serializers

from stats.models import Country, LiveStatistic


class LiveStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveStatistic
        fields = ('date', 'new_cases', 'new_deaths', 'active_cases',
                  'critical', 'total_cases', 'total_deaths', 'total_recovered',
                  'total_tests')


class CountrySerializer(serializers.ModelSerializer):
    statistics = serializers.SerializerMethodField()

    def get_statistics(self, obj: Country) -> dict:
        query = LiveStatistic.objects.filter(country=obj.id,
                                             date__gte=datetime.date.today())
        serializer = LiveStatisticSerializer(query, many=True)
        return serializer.data

    class Meta:
        model = Country
        fields = ('id', 'name', 'statistics')
