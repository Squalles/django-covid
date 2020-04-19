from django.core.management.base import BaseCommand, CommandError

from covid19.utils.scraper.worldmeter import TableScraper


class Command(BaseCommand):
    help = 'Command for fetching Coronavirus statistics'

    def handle(self, *args, **options):
        ts = TableScraper()
        ts.scrap()
