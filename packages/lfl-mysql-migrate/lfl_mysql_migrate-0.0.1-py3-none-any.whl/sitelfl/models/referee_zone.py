from django.db import models


class RefereeZone(models.Model):
    league_id = models.IntegerField()
    referee_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'referee_zone'
        unique_together = (('referee_id', 'league_id'),)
