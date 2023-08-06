from django.db import models


class Penalties(models.Model):
    action = models.IntegerField(blank=True, null=True)
    club_id = models.IntegerField()
    edited_by_id = models.IntegerField(blank=True, null=True)
    last_edit_date = models.DateTimeField(blank=True, null=True)
    match_id = models.IntegerField()
    minute = models.IntegerField()
    penalty_id = models.AutoField(primary_key=True)
    player_id = models.IntegerField()
    referee_id = models.IntegerField()
    result = models.IntegerField()
    tournament_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'penalties'
