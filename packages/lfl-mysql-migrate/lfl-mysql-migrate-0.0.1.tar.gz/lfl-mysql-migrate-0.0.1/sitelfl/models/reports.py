from django.db import models


class Reports(models.Model):
    match_id = models.IntegerField(primary_key=True)
    weather = models.CharField(max_length=100, blank=True, null=True)
    audience = models.IntegerField()
    home_captian = models.IntegerField(blank=True, null=True)
    away_captian = models.IntegerField(blank=True, null=True)
    home_optimum = models.IntegerField(blank=True, null=True)
    away_optimum = models.IntegerField(blank=True, null=True)
    star1 = models.IntegerField(blank=True, null=True)
    star2 = models.IntegerField(blank=True, null=True)
    star3 = models.IntegerField(blank=True, null=True)
    report = models.CharField(max_length=1000, blank=True, null=True)
    last_edit_date = models.DateTimeField(blank=True, null=True)
    edited_by_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reports'
