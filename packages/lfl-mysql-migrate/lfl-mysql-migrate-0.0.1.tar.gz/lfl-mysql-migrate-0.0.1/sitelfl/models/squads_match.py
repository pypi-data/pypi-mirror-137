from django.db import models


class SquadsMatch(models.Model):
    match_id = models.IntegerField()
    number = models.IntegerField()
    player_id = models.IntegerField()
    squads_match_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'squads_match'
        unique_together = (('match_id', 'player_id'),)
