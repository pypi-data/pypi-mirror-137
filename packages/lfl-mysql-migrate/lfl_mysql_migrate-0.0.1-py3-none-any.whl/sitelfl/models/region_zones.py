from django.db import models


class RegionZones(models.Model):
    active = models.IntegerField()
    contacts = models.TextField()
    edited_by_id = models.IntegerField()
    geo = models.CharField(max_length=255)
    level = models.IntegerField()
    logo = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    parent_id = models.IntegerField()
    region_zone_id = models.AutoField(primary_key=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'region_zones'
