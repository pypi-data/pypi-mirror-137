from django.db import models


class Fouls(models.Model):
    club_id = models.IntegerField()
    edited_by_id = models.IntegerField()
    foul_id = models.AutoField(primary_key=True)
    last_edit_date = models.DateTimeField(blank=True, null=True)
    match_id = models.IntegerField()
    minute = models.IntegerField()
    penalty = models.IntegerField()
    player_id = models.IntegerField()
    tournament_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'fouls'
