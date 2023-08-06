import logging

from django.core.management import BaseCommand

from sitelfl.management.commands import migrate_base

logger = logging.getLogger( __name__ )


class Command( BaseCommand ) :
    help = "Перенос данных"

    def add_arguments( self , parser ) :
        parser.add_argument( '--mode' , type=str )

    def handle( self , *args , **options ) :
        mode = options.get( 'mode' )

        logger.info( self.help )

        migrate_base( mode=mode )
