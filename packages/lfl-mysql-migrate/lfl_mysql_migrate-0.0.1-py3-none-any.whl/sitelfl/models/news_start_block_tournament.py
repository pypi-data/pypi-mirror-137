from django.db import models
from django.db.models import BigIntegerField


class NewsStartBlockTournament(models.Model):
    active = models.IntegerField()
    admin_id = models.IntegerField()
    comment = models.CharField(max_length=256, blank=True, null=True)
    created_by = models.IntegerField()
    date = models.DateTimeField(blank=True, null=True)
    disable_editor = models.IntegerField(blank=True, null=True)
    id = BigIntegerField(primary_key=True)
    in_middle = models.IntegerField()
    in_top = models.IntegerField()
    last_edit_date = models.DateTimeField(blank=True, null=True)
    preamble = models.TextField(blank=True, null=True)
    tournament_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'news_start_block_tournament'
