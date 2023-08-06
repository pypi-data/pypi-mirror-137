from django.db import models


class TournamentMembers(models.Model):
    tournament_id = models.IntegerField(primary_key=True)
    club_id = models.IntegerField()
    position = models.IntegerField()
    game_over = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tournament_members'
        unique_together = (('tournament_id', 'club_id'),)
