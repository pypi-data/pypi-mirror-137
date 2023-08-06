from django.db import models


class PlayerTournamentCardsLimit(models.Model):
    card_type = models.CharField(max_length=3)
    count = models.SmallIntegerField()
    player_id = models.IntegerField()
    tournament_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'player_tournament_cards_limit'
        unique_together = (('player_id', 'tournament_id'),)
