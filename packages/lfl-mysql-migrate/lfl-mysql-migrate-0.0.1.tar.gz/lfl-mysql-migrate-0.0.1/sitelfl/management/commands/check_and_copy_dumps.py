import logging
import os
from os import walk
from pathlib import Path
from shutil import copy2

from django.core.management import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Проверка количества дампов MySql"

    def handle(self, *args, **options):
        print(self.help)

        c_dumps_path = 'C:\dumps'
        d_dumps_path = 'D:\dumps'

        c_files = []
        for (dirpath, dirnames, filenames) in list(walk(c_dumps_path)):
            for filename in filenames:
                full_path_source = f'{dirpath}{os.sep}{filename}'

                stat_source = Path(full_path_source).stat()
                st_mtime = stat_source.st_mtime
                c_files.append((full_path_source, st_mtime))

        c_files.sort(key=lambda x: x[1], reverse=True)
        c_max_qty = 700
        d_max_qty = 80

        i = 1
        c_files_odd = []
        for file, st_mtime in c_files:
            if i > c_max_qty:
                os.remove(file)
                print(f'({i}) file: {file}, removed.')
            else:
                c_files_odd.append((file, st_mtime))
            i += 1

        d_files = []
        for (dirpath, dirnames, filenames) in list(walk(d_dumps_path)):
            for filename in filenames:
                full_path_source = f'{dirpath}{os.sep}{filename}'

                stat_source = Path(full_path_source).stat()
                st_mtime = stat_source.st_mtime
                d_files.append((full_path_source, st_mtime))

        d_files.sort(key=lambda x: x[1], reverse=True)
        d_files_qty = len(d_files)
        i = 1
        for file, st_mtime in d_files:
            if i > d_max_qty:
                os.remove(file)
                print(f'({i}) file: {file}, removed.')
            i += 1

        i = 1
        c_files_odd.sort(key=lambda x: x[1], reverse=True)
        if d_files_qty < d_max_qty:
            d_files_qty = d_max_qty - d_files_qty
            for file, st_mtime in c_files_odd:
                if i > d_files_qty:
                    break

                dst = file.replace(c_dumps_path, d_dumps_path)
                if not os.path.exists(dst):
                    copy2(src=file, dst=dst)
                    print(f'({i}) file: {file}, copied.')
                    i += 1

        elif d_files_qty == d_max_qty:
            for i in range(len(c_files_odd) - 1):
                file = c_files_odd[i][0]
                file_d = file.replace(c_dumps_path, d_dumps_path)

                if not os.path.exists(file_d):
                    os.remove(d_files[len(d_files) - (i + 1)][0])
                    copy2(src=file, dst=file_d)
                    print(f'({i}) file: {file}, copied.')
                    break

        logger.info('Done.')
