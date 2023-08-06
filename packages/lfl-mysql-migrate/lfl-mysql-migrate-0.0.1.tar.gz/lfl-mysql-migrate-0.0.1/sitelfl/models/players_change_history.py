from django.db import models


class PlayersChangeHistory(models.Model):
    data = models.CharField(max_length=512)
    date = models.DateTimeField(primary_key=True)
    editor_id = models.IntegerField()
    player_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'players_change_history'
        unique_together = (('date', 'editor_id', 'player_id'),)
