from django.db import models


class MenuZones(models.Model):
    menu_zone_id = models.AutoField(primary_key=True)
    menu_id = models.IntegerField()
    zone_type = models.IntegerField()
    zone_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'menu_zones'
