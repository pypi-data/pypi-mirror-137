from django.db import models


class RefereeCategory(models.Model):
    active = models.IntegerField()
    edited_by_id = models.IntegerField()
    name = models.CharField(max_length=255)
    priority = models.IntegerField()
    referee_category_id = models.AutoField(primary_key=True)
    region_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'referee_category'
