from django.db import models


class MenuOld(models.Model):
    active = models.IntegerField()
    type = models.IntegerField()
    region_id = models.IntegerField()
    league_id = models.IntegerField()
    parent_id = models.IntegerField()
    level = models.IntegerField()
    position = models.IntegerField()
    name = models.CharField(max_length=32, blank=True, null=True)
    subname = models.CharField(max_length=64, blank=True, null=True)
    columns = models.IntegerField()
    link = models.CharField(max_length=100)
    style = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    blank = models.IntegerField()
    cookies = models.CharField(max_length=256)
    last_edit_date = models.DateTimeField(blank=True, null=True)
    edited_by_id = models.IntegerField(blank=True, null=True)
