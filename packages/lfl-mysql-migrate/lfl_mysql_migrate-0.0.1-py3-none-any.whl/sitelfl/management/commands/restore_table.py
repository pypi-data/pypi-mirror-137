import logging

from django.core.management import BaseCommand
from django.db import transaction

from lfl_admin.competitions.models.referees import Referees
from sitelfl.models.persons import Persons as OldPersons

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Восстановление данных"

    def handle(self, *args, **options):
        logger.info(self.help)

        # ============================ referees ===============================
        referees = []
        with transaction.atomic():
            RefereesQuery = Referees.objects.filter(old_ids__overlap=[1727]).order_by('id')
            # pbar = tqdm(total=RefereesQuery.count())

            # image_type_photo11 = Image_types.objects.get(code='photo11')
            # image_type_photo2 = Image_types.objects.get(code='photo2')
            # image_type_photo3 = Image_types.objects.get(code='photo3')
            cnt = 0
            for referee in RefereesQuery:
                if len(referee.person.old_ids) > 1:
                    for referee_old_id in referee.old_ids:
                        print(f'referee_id: {referee_old_id}')
                        referees.append((referee_old_id, 0))
                        for person_old_id in referee.person.old_ids:
                            person = OldPersons.objects.using('sitelfl').get(person_id=person_old_id)
                            print(f'  {person}')

                        cnt += 1

                #
                #     active = 0
                #     if referee.props._value == Referees.props.active:
                #         active = 1
                #     user = referee.person.user
                #
                #     images_photo11 = Referees_images.objects.getOptional(main_model=referee, image__image_type=image_type_photo11)
                #     images_photo2 = Referees_images.objects.getOptional(main_model=referee, image__image_type=image_type_photo2)
                #     images_photo3 = Referees_images.objects.getOptional(main_model=referee, image__image_type=image_type_photo3)
                #
                #     OldReferees.objects.using('sitelfl').create(
                #         active=active,
                #         birthday1=user.birthday,
                #         contact_id=referee.contact.old_id if referee.contact is not None else 0,
                #         debut=referee.debut,
                #         # edited_by_id = models.IntegerField(blank=True, null=True)
                #         family_name1=user.last_name,
                #         first_name1=user.first_name,
                #         last_edit_date=referee.lastmodified,
                #         person_id=referee.person.old_ids[0],
                #         photo11=images_photo11.image.olnly_real_file_name if images_photo11 is not None else '',
                #         photo2=images_photo11.image.olnly_real_file_name if images_photo2 is not None else '',
                #         photo3=images_photo11.image.olnly_real_file_name if images_photo3 is not None else '',
                #         referee_id=refere_old_id,
                #         referee_post=referee.referee_post.name,
                #         region_id=referee.region.old_id if referee.region is not None else 0,
                #         second_name1=user.middle_name,
                #         unique_id=refere_old_id
                #     )
                # pbar.update()
        # ============================= End referees ==========================

        # with transaction.atomic():
        #     RefereesQuery = OldReferees.objects.using('sitelfl').all()
        #     pbar = tqdm(total=RefereesQuery.count())
        #     for referee in RefereesQuery:
        #         try:
        #             person = OldPersons.objects.using('sitelfl').get(
        #                 active=1,
        #                 first_name=referee.first_name1,
        #                 second_name=referee.second_name1,
        #                 family_name=referee.family_name1,
        #                 birthday=referee.birthday1,
        #                 region_id=referee.region_id
        #             )
        #         except OldPersons.MultipleObjectsReturned:
        #             persons = list(OldPersons.objects.using('sitelfl').filter(
        #                 active=1,
        #                 first_name=referee.first_name1,
        #                 second_name=referee.second_name1,
        #                 family_name=referee.family_name1,
        #                 birthday=referee.birthday1,
        #                 region_id=referee.region_id
        #             ).order_by('person_id'))
        #             if not referee.person_id in list(map(lambda x: x.person_id, persons)):
        #                 person = persons[0]
        #             else:
        #                 pbar.update()
        #                 continue
        #
        #         except OldPersons.DoesNotExist:
        #             try:
        #                 person = OldPersons.objects.using('sitelfl').get(
        #                     active=1,
        #                     first_name=referee.first_name1,
        #                     second_name=referee.second_name1,
        #                     family_name=referee.family_name1,
        #                     birthday=referee.birthday1,
        #                 )
        #             except OldPersons.MultipleObjectsReturned:
        #                 persons = list(OldPersons.objects.using('sitelfl').filter(
        #                     active=1,
        #                     first_name=referee.first_name1,
        #                     second_name=referee.second_name1,
        #                     family_name=referee.family_name1,
        #                     birthday=referee.birthday1,
        #                 ).order_by('person_id'))
        #                 if not referee.person_id in list(map(lambda x: x.person_id, persons)):
        #                     person = persons[0]
        #                 else:
        #                     pbar.update()
        #                     continue
        #
        #             except OldPersons.DoesNotExist:
        #                 try:
        #                     person = OldPersons.objects.using('sitelfl').get(
        #                         first_name=referee.first_name1,
        #                         second_name=referee.second_name1,
        #                         family_name=referee.family_name1,
        #                         birthday=referee.birthday1
        #                     )
        #                 except OldPersons.DoesNotExist:
        #                     try:
        #                         person = OldPersons.objects.using('sitelfl').get(
        #                             first_name=referee.first_name1,
        #                             second_name=referee.second_name1,
        #                             family_name=referee.family_name1,
        #                         )
        #                     except OldPersons.DoesNotExist:
        #                         pbar.update()
        #                         continue
        #
        #         if person.person_id != referee.person_id:
        #             # referee.person_id = person.person_id
        #             # referee.save()
        #             print(person.person_id)
        #         pbar.update()

        print(f'Done: {cnt}')
        print(referees)
