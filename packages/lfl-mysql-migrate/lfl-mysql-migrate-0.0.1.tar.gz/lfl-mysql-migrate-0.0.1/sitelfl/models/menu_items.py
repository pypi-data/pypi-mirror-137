from django.db import models
from django.db.models import BigIntegerField


class MenuItems(models.Model):
    active = models.IntegerField(blank=True, null=True)
    id = BigIntegerField(primary_key=True)
    img = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    target = models.IntegerField(blank=True, null=True)
    url = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'menu_items'
