from django.db import models


class MatchStats(models.Model):
    away_value = models.IntegerField()
    home_value = models.IntegerField()
    match_id = models.IntegerField()
    stat_key = models.CharField(max_length=30)
    stat_title = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'match_stats'
