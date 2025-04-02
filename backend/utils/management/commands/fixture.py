from django.core.management.base import BaseCommand, CommandError
from utils import fixtures


class Command(BaseCommand):
    help = "Create fixtures"

    # def add_arguments(self, parser):
    #     parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        fixtures.main()
        try:
            #fixtures.main()
            ...
        except:
            raise CommandError('Fixture encountered an error')

