from django.db import models
from django.db.models import BigIntegerField


class MenuItemLeagues(models.Model):
    id = BigIntegerField(primary_key=True)
    league_id = models.IntegerField(blank=True, null=True)
    menu_item = models.ForeignKey('MenuItems', models.DO_NOTHING)
    region_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'menu_item_leagues'
