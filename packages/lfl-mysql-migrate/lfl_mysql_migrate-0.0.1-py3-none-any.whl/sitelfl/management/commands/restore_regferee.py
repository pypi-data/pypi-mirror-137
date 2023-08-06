import logging

from django.core.management import BaseCommand
from django.db import transaction
from tqdm import tqdm

from isc_common import delAttr1, setAttr
from isc_common.number import model_2_dict
from sitelfl.models.persons import Persons
from sitelfl.models.referees import Referees

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Восстановление данных"

    def handle(self, *args, **options):
        logger.info(self.help)

        # ============================ referees ===============================
        with transaction.atomic():
            query = Referees.objects.using('sitelfl-old').filter()
            pbar = tqdm(total=query.count())

            for referee in query:
                try:
                    Persons.objects.using('sitelfl').get(person_id=referee.person_id)
                except Persons.DoesNotExist:
                    try:
                        kwargs = delAttr1(model_2_dict(Persons.objects.using('sitelfl-old').get(person_id=referee.person_id)), 'person_id')
                        person = Persons.objects.using('sitelfl').create(**kwargs)
                        setAttr(kwargs, 'person_id', person.person_id)
                    except Persons.DoesNotExist:
                        continue

                kwargs = delAttr1(model_2_dict(referee), 'referee_id')

                try:
                    referee_ex = Referees.objects.using('sitelfl').get(referee_id=referee.referee_id)
                    if referee_ex.person_id != referee.person_id:
                        Referees.objects.using('sitelfl').filter(referee_id=referee.referee_id).update(**kwargs)
                        print(f'Updated: {referee_ex}')
                except Referees.DoesNotExist:
                    referee_ex = Referees.objects.using('sitelfl').create(**kwargs)
                    print(f'Created: {referee_ex}')

                pbar.update()
