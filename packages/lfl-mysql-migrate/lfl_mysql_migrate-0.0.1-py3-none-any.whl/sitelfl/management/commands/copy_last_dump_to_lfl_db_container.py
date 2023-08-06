import logging
import os

from django.core.management import BaseCommand

from isc_common.ssh.ssh_client import SSH_Client

logger = logging.getLogger(__name__)


def copy_newest_file(
        host='176.107.243.22',
        port=22,
        user='ayudin',
        password='cfdtkbq',
        dumps_path='/home/lfl-db-dumps/dumps-mysql',
        localpath='/home/lfl-old-mysql/dumps-mysql'
):
    ssh_client = SSH_Client(hostname=host, username=user, password=password, port=port)

    c_files = []

    for filename in ssh_client.listdir(dumps_path):
        full_path_source = f'{dumps_path}{os.sep}{filename}'
        st_mtime = ssh_client.stat(path=full_path_source).st_mtime
        c_files.append((full_path_source, st_mtime))

    c_files.sort(key=lambda x: x[1], reverse=True)
    file, _ = c_files[0]

    _, only_file = os.path.split(file)

    print('Start coping')
    ssh_client.get(remotepath=file, localpath=f'{localpath}{os.sep}dump.sql')
    print('Done.')


class Command(BaseCommand):
    help = "Восстановление данных"

    def handle(self, *args, **options):
        copy_newest_file()
