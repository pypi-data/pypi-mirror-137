from django.db import models


class Fields(models.Model):
    active = models.IntegerField()
    edited_by_id = models.IntegerField()
    field_id = models.AutoField(primary_key=True)
    height = models.IntegerField()
    image = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    width = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'fields'
