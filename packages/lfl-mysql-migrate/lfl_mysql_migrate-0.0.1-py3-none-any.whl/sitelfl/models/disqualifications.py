from django.db import models


class Disqualifications(models.Model):
    active = models.IntegerField()
    admin_id = models.IntegerField(blank=True, null=True)
    card_id = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    disqualification_id = models.AutoField(primary_key=True)
    disqualification_type = models.CharField(max_length=4, blank=True, null=True)
    edit_date = models.DateTimeField(blank=True, null=True)
    from_date = models.DateTimeField(blank=True, null=True)
    matches = models.IntegerField(blank=True, null=True)
    note = models.CharField(max_length=150, blank=True, null=True)
    personal_league_id = models.IntegerField()
    personal_region_id = models.IntegerField()
    personal_tournament_id = models.IntegerField()
    player_id = models.IntegerField()
    to_date = models.DateField(blank=True, null=True)
    tournament_id = models.IntegerField()
    zone_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'disqualifications'
