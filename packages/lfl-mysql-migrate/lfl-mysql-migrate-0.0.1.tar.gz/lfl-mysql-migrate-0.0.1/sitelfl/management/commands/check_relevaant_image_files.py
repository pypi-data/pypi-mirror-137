import logging
import os.path

from django.conf import settings
from django.core.management import BaseCommand
from isc_common import Stack
from isc_common.models.images import Images
from tqdm import tqdm

logger = logging.getLogger( __name__ )


class Command( BaseCommand ) :
    help = "Проверка наличия файлов в старом хранилище"

    def handle( self , *args , **options ) :
        ssh_client = settings.SSH_CLIENTS.client( settings.FILES_STORE )
        files_exists = Stack()
        files_nexists = Stack()

        query = Images.objects.exclude( attfile='' )
        pbar = tqdm( total=query.count() )

        for image in query :
            dir , file = os.path.split( str( image.attfile ) )
            _file = f'{settings.FILES_STORE.get( "PATH" )}{os.sep}{file}'
            if ssh_client.exists( _file ) :
                files_exists.push( file )

                if dir != '' :
                    image.attfile = file
                    image.save()
            else :
                image.attfile = ''
                image.size = 0
                image.save()

                files_nexists.push( file )

            pbar.update()

        files_exists.extend( files_nexists )
        i = 0;
        excluded = [ '.git' , 'tmp' , '.gitignore' ]
        for file in ssh_client.listdir( settings.FILES_STORE.get( "PATH" ) ) :
            if file not in files_exists.stack :
                if file not in excluded :
                    old_file = f'{settings.FILES_STORE.get( "PATH" )}{os.sep}{file}'
                    new_file = f'{settings.UNBOUNDED_FILES}{os.sep}{file}'
                    ssh_client.rename( oldpath=old_file , newpath=new_file )
                    print( f'# {i} {file}' )
                    i += 1
