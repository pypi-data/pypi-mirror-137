from django.db import models


class Goals(models.Model):
    assist_id = models.IntegerField(blank=True, null=True)
    club_id = models.IntegerField()
    edited_by_id = models.IntegerField(blank=True, null=True)
    goal_club_id = models.IntegerField()
    goal_id = models.AutoField(primary_key=True)
    goal_type = models.IntegerField()
    last_edit_date = models.DateTimeField(blank=True, null=True)
    match_id = models.IntegerField()
    minute = models.IntegerField(blank=True, null=True)
    player_id = models.IntegerField()
    tournament_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'goals'
