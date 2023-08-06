from django.db import models
from django.db.models import BigIntegerField


class Menu(models.Model):
    active = models.IntegerField()
    blank = models.IntegerField()
    columns = models.IntegerField()
    cookies = models.CharField(max_length=256)
    edited_by_id = models.IntegerField(blank=True, null=True)
    id = BigIntegerField(primary_key=True)
    image = models.CharField(max_length=255)
    last_edit_date = models.DateTimeField(blank=True, null=True)
    league_id = models.IntegerField()
    level = models.IntegerField()
    link = models.CharField(max_length=100)
    name = models.CharField(max_length=32, blank=True, null=True)
    parent_id = models.IntegerField()
    position = models.IntegerField()
    region_id = models.IntegerField()
    style = models.CharField(max_length=255)
    subname = models.CharField(max_length=64, blank=True, null=True)
    type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'menu'
