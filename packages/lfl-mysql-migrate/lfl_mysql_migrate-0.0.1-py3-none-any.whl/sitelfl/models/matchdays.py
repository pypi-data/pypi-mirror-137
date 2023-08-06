from django.db import models


class Matchdays(models.Model):
    date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    tour = models.IntegerField()
    tournament_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'matchdays'
        unique_together = (('tournament_id', 'tour'),)
