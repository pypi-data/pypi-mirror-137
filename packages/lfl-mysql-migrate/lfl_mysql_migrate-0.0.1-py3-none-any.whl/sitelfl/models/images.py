from django.db import models
from isc_common.managers.common_manager import ExtManager


class Images(models.Model):
    image_id = models.AutoField(primary_key=True)
    image_path = models.CharField(max_length=256)
    type = models.CharField(max_length=10)

    objects = ExtManager()

    class Meta:
        managed = False
        db_table = 'images'
