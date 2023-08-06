from django.db import models


class DisqualificationZones(models.Model):
    zone_id = models.AutoField(primary_key=True)
    region_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=128)
    active = models.IntegerField()
    number_of_yellowsold = models.IntegerField(db_column='number_of_yellowsOLD')  # Field name made lowercase.
    last_edit_date = models.DateTimeField(blank=True, null=True)
    edited_by_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'disqualification_zones'
