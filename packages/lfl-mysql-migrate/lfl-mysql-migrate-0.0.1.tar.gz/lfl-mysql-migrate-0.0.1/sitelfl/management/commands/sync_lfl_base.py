import logging
import os
import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management import BaseCommand
from django.db import connections

from isc_common.string import BytesToStr
from sitelfl.management.commands.copy_last_dump_to_lfl_db_container import copy_newest_file

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Синхронизация данных"

    def print_std_out(self, stdout, stderr):
        res_str = []
        for st in BytesToStr(stdout).split('\n'):
            res_str.append(st)

        if len(res_str) > 0:
            for s in res_str:
                print(s)
            return True
        return False

    def handle(self, *args, **options):

        copy_newest_file(host='192.168.0.237', user='lfl-db-dumps', password='lfl-db-dumps')

        c_files = []
        print('Import MySQL DB dump. See import.log')
        for (dirpath, dirnames, filenames) in list(os.walk(settings.C_DUMPS_PATH)):
            for filename in filenames:
                full_path_source = f'{dirpath}{os.sep}{filename}'

                stat_source = Path(full_path_source).stat()
                st_mtime = stat_source.st_mtime
                c_files.append((full_path_source, st_mtime))

        c_files.sort(key=lambda x: x[1], reverse=True)
        file, _ = c_files[0]
        dir, _ = os.path.split(file)

        command = f'''{settings.MYSQL} {settings.MYQL_DATABASE} -u{settings.MYQL_USERNAME} -p{settings.MYQL_PASSWORD} -v < {file}'''

        with open('logs/import.log', 'wb') as f:
            process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for c in iter(lambda: process.stdout.read(1), b''):
                f.write(c)

        print('Alter MySQL tables. See debug.log')
        with connections['sitelfl'].cursor() as cursor:
            logger.debug(f'Altering keepers')
            cursor.execute('''ALTER TABLE keepers ADD comp_ids varchar(255) AFTER edited_by_id''')
            cursor.execute('''CREATE INDEX keepers_comp_ids_idx ON keepers (comp_ids)''')
            cursor.execute('''UPDATE keepers set comp_ids = concat(match_id, '_', player_id, '_', tournament_id)''')
            logger.debug(f'Altered keepers')

            logger.debug(f'Altering player_histories')
            cursor.execute('''ALTER TABLE player_histories ADD comp_ids varchar(255) AFTER edited_by_id''')
            cursor.execute('''CREATE INDEX player_histories_comp_ids_idx ON player_histories (comp_ids)''')
            cursor.execute('''UPDATE player_histories set comp_ids =  concat(match_id, '_', player_id, '_', club_id)''')
            logger.debug(f'Altered player_histories')

            logger.debug(f'Altering squads')
            cursor.execute('''ALTER TABLE squads ADD comp_ids varchar(255) AFTER edited_by_id''')
            cursor.execute('''CREATE INDEX squads_comp_ids_idx ON squads (comp_ids)''')
            cursor.execute('''UPDATE squads set comp_ids =  concat(player_id, '_', club_id, '_', tournament_id)''')
            logger.debug(f'Altered squads')

        print('Migrate DB. See debug.log')
        # migrate_base('all')

        print('Done.')
