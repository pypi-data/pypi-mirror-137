from django.db import models
from django.db.models import CharField


class Keepers( models.Model ) :
    club_id = models.IntegerField()
    edited_by_id = models.IntegerField( blank=True , null=True )
    goals = models.IntegerField()
    last_edit_date = models.DateTimeField( blank=True , null=True )
    match_id = models.IntegerField( primary_key=True )
    player_id = models.IntegerField()
    tournament_id = models.IntegerField()
    comp_ids = CharField( max_length=255 , null=True , blank=True , db_index=True )

    class Meta :
        managed = False
        db_table = 'keepers'
        unique_together = (('match_id' , 'tournament_id' , 'player_id') ,)
