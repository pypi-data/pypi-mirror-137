from django.db import models


class CityRegions(models.Model):
    city_region_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'city_regions~'
