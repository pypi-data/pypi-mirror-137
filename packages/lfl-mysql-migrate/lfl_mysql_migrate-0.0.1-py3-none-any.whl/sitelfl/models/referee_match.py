from django.db import models


class RefereeMatch(models.Model):
    match_id = models.IntegerField()
    referee_id = models.IntegerField()
    referee_match_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'referee_match'
