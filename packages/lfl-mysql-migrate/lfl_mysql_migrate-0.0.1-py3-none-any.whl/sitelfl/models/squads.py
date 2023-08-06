from django.db import models
from django.db.models import CharField


class Squads(models.Model):
    club_id = models.IntegerField(primary_key=True)
    comment = models.CharField( max_length=255 , blank=True , null=True )
    comp_ids = CharField( max_length=255 , null=True , blank=True , db_index=True )
    deducted = models.DateField( blank=True , null=True )
    edited_by_id = models.IntegerField(blank=True, null=True)
    included = models.DateField(blank=True, null=True)
    last_edit_date = models.DateTimeField(blank=True, null=True)
    player_id = models.IntegerField()
    tournament_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'squads'
        unique_together = (('club_id', 'tournament_id', 'player_id'),)
