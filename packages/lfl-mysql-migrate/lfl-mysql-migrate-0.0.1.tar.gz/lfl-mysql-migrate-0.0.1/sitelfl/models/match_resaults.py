from django.db import models


class MatchResaults(models.Model):
    away_score = models.IntegerField()
    home_score = models.IntegerField()
    match_id = models.IntegerField()
    resault_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'match_resaults'
        unique_together = (('match_id', 'user_id'),)
