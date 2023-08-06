import logging

from django.conf import settings
from django.core.management import BaseCommand
from isc_common.fields.files import make_REPLACE_IMAGE_PATH
from isc_common.managers.common_manager import lazy_bulk_fetch
from lfl_admin.common.models.site_lfl_images import Site_lfl_images
from tqdm import tqdm

logger = logging.getLogger( __name__ )


class Command( BaseCommand ) :
    help = "Проверка наличия файлов в старом хранилище"

    def handle( self , *args , **options ) :
        query = Site_lfl_images.objects.all()
        qnt = query.count()
        print( qnt )
        pbar = tqdm( total=qnt )
        # print( pbar )

        fetcher = lazy_bulk_fetch( 100 , qnt , lambda : Site_lfl_images.objects.order_by( 'id' ) )
        b = 1
        for batch in fetcher :
            # print( f'\nBatch# {b}' )
            for file in Site_lfl_images.objects.raw( str( batch.query ) ) :
                file_fullpath = make_REPLACE_IMAGE_PATH( file.path )
                if settings.SSH_CLIENT.exists( file_fullpath ) is False :
                    logger.debug( f'Deliting : {file}' )
                    file.delete()
                pbar.update()
            b += 1

        logger.info( 'Done.' )
