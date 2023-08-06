from django.db import models


class TournamentMemberDoubles(models.Model):
    club_double_id = models.IntegerField()
    club_id = models.IntegerField()
    edited_by_id = models.IntegerField(blank=True, null=True)
    last_edit_date = models.DateTimeField(blank=True, null=True)
    tournament_double_id = models.IntegerField()
    tournament_id = models.IntegerField()
    tournament_member_double_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'tournament_member_doubles'
        unique_together = (('tournament_double_id', 'club_double_id'),)
