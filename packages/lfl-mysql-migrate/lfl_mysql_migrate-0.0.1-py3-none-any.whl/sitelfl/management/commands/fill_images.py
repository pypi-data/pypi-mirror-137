import logging
import os
from os import walk
from pathlib import Path

from django.core.management import BaseCommand
from lfl_admin.common.models.site_lfl_images import Site_lfl_images
from tqdm import tqdm

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Заполнение данных по изображениям"

    def handle(self, *args, **options):
        print(self.help)

        source_path = 'C:\lflru'
        i = 0

        excl = ['.git', '.idea', 'TmpFile1', 'Programs', 'tmp']

        point_length = 70
        cnt = point_length
        for (dirpath, dirnames, filenames) in walk(source_path):
            for filename in filenames:
                full_path_source = f'{dirpath}{os.sep}{filename}'
                exclude = len(list(filter(lambda x: dirpath.find(x) != -1, excl))) > 0
                if exclude is False:
                    exclude = len(list(filter(lambda x: full_path_source.find(x) != -1, excl))) > 0
                if exclude is True:
                    continue

                _, dir = os.path.splitext(filename)

                if dir in ['.gif', '.png', '.jpg', '.jpeg']:
                    stat_source = Path(full_path_source).stat()
                    print_nol = False
                    try:
                        site_lfl_image = Site_lfl_images.objects.get(path=full_path_source)
                        if site_lfl_image.date != stat_source.st_mtime:
                            site_lfl_image.date = stat_source.st_mtime
                            site_lfl_image.save()

                            if print_nol is True:
                                print(f'\nUpdated ({i}): {full_path_source}')
                                print_nol = False
                            else:
                                print(f'Updated ({i}): {full_path_source}')
                            cnt = point_length
                        else:
                            print_nol = True
                            if cnt == 0:
                                print('.')
                                cnt = point_length
                            else:
                                print('.', end='')
                                cnt -= 1
                    except Site_lfl_images.DoesNotExist:
                        Site_lfl_images.objects.create(
                            path=full_path_source,
                            file_name=filename,
                            date=stat_source.st_mtime
                        )

                        if print_nol is True:
                            print(f'\nApended ({i}): {full_path_source}')
                            print_nol = False
                        else:
                            print(f'Apended ({i}): {full_path_source}')
                        cnt = point_length

                    i += 1

        # site_lfl_images_query = Site_lfl_images.objects.filter()
        # pbar = tqdm(total=site_lfl_images_query.count())
        #
        # i = 0
        # for site_lfl_image in site_lfl_images_query:
        #     if not os.path.exists(site_lfl_image.path):
        #         logger.debug(f'{site_lfl_image.path} not found an delete.')
        #         site_lfl_image.delete()
        #         i += 1
        #     pbar.update()
        # pbar.close()
        #
        # print(f'Done. Deleted: {i}, All: {site_lfl_images_query.count()}')
