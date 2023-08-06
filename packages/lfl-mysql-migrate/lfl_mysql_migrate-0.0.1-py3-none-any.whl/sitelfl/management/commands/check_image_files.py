import logging

from django.core.management import BaseCommand
from isc_common.common.functions import check_image_files

logger = logging.getLogger( __name__ )


class Command( BaseCommand ) :
    help = "Проверка наличия файлов в старом хранилище"

    def handle( self , *args , **options ) :
        check_image_files( None , None )
