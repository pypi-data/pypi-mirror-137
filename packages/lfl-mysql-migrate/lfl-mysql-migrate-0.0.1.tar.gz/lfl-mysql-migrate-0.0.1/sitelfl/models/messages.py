from django.db import models


class Messages(models.Model):
    message_id = models.AutoField(primary_key=True)
    region_id = models.IntegerField()
    date = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=30, blank=True, null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)
    image_link = models.CharField(max_length=100, blank=True, null=True)
    active = models.IntegerField()
    stadium_id = models.IntegerField(blank=True, null=True)
    author = models.IntegerField(blank=True, null=True)
    top = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'messages'
