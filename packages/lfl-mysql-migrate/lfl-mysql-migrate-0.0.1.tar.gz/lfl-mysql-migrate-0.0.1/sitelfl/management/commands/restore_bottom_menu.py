import logging

from django.core.management import BaseCommand
from django.db import transaction

from lfl_admin.competitions.models.referees import Referees
from tqdm import tqdm

from sitelfl.models.bottom_menu import Bottom_menu
from sitelfl.models.persons import Persons as OldPersons

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Восстановление данных"

    def handle(self, *args, **options):
        logger.info(self.help)

        with transaction.atomic():
            cnt = Bottom_menu.objects.using('sitelfl').count()
            Bottom_menuQuery = Bottom_menu.objects.using('sitelfl-test').exclude(id__in=map(lambda x: x.id, Bottom_menu.objects.using('sitelfl'))).order_by('id')
            pbar = tqdm(total=Bottom_menuQuery.count())

            for bottom_menu in Bottom_menuQuery:
                Bottom_menu.objects.using('sitelfl').create(
                    id=bottom_menu.id,
                    parent_id=bottom_menu.parent_id,
                    position=bottom_menu.position,
                    name=bottom_menu.name,
                    url=bottom_menu.url,
                    type=bottom_menu.type,
                )
                pbar.update()

        print(f'Done')
