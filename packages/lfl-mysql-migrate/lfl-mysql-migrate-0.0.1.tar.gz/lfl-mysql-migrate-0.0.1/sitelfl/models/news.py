from django.db import models
from django.db.models import BigIntegerField


class News(models.Model):
    active = models.IntegerField()
    admin_id = models.IntegerField()
    attache_dir = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=256, blank=True, null=True)
    created_by = models.IntegerField()
    date = models.DateTimeField(blank=True, null=True)
    disable_editor = models.IntegerField(blank=True, null=True)
    en_id = models.IntegerField(blank=True, null=True)
    external_link = models.CharField(max_length=256, blank=True, null=True)
    fixed_position = models.SmallIntegerField()
    icon = models.IntegerField(blank=True, null=True)
    id = BigIntegerField(primary_key=True)
    image_big_id = models.IntegerField()
    image_path = models.CharField(max_length=1024, blank=True, null=True)
    image_small_id = models.IntegerField()
    imageshort = models.CharField(max_length=1024, blank=True, null=True)
    in_bottom = models.IntegerField()
    in_middle = models.IntegerField()
    in_top = models.IntegerField()
    last_edit_date = models.DateTimeField(blank=True, null=True)
    league_id = models.IntegerField()
    link = models.CharField(max_length=1024, blank=True, null=True)
    match_id = models.IntegerField(blank=True, null=True)
    position = models.IntegerField()
    preamble = models.TextField(blank=True, null=True)
    region_id = models.IntegerField()
    text = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    tour = models.CharField(max_length=32)
    tournament_id = models.IntegerField()
    type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'news'
