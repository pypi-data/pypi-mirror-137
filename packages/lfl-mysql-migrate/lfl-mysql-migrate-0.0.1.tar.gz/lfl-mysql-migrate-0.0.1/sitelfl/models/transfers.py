from django.db import models


class Transfers(models.Model):
    transfer_id = models.AutoField(primary_key=True)
    player_id = models.IntegerField()
    from_club = models.IntegerField()
    to_club = models.IntegerField()
    next_prev_club = models.IntegerField()
    transfer_date = models.DateField(blank=True, null=True)
    leasing_days = models.IntegerField(blank=True, null=True)
    last_edit_date = models.DateTimeField(blank=True, null=True)
    edited_by_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transfers'
