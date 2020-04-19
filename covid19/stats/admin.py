from django.contrib import admin

from stats.models import Country, LiveStatistic


class CountryAdmin(admin.ModelAdmin):
    pass


class LiveStatisticAdmin(admin.ModelAdmin):
    pass


admin.site.register(Country, CountryAdmin)
admin.site.register(LiveStatistic, LiveStatisticAdmin)
