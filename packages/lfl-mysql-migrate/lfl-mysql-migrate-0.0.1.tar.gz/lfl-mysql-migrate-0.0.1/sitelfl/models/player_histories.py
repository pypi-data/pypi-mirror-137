from django.db import models
from django.db.models import CharField


class PlayerHistories(models.Model):
    club_id = models.IntegerField()
    edited_by_id = models.IntegerField(blank=True, null=True)
    formation = models.IntegerField()
    game_started = models.IntegerField()
    keeper = models.IntegerField(blank=True, null=True)
    last_edit_date = models.DateTimeField(blank=True, null=True)
    match_id = models.IntegerField()
    player_id = models.IntegerField(primary_key=True)
    substituted = models.IntegerField()
    tournament_id = models.IntegerField()
    comp_ids = CharField( max_length=255 , null=True , blank=True , db_index=True )

    class Meta:
        managed = False
        db_table = 'player_histories'
        unique_together = (('player_id', 'match_id', 'club_id'),)
