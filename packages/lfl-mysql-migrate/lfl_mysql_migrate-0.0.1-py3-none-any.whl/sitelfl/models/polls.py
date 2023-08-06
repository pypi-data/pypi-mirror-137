from django.db import models


class Polls(models.Model):
    active = models.IntegerField()
    edited_by_id = models.IntegerField()
    max_answers = models.IntegerField()
    min_answers = models.IntegerField()
    name = models.CharField(max_length=255)
    poll_id = models.AutoField(primary_key=True)
    text = models.TextField()

    class Meta:
        managed = False
        db_table = 'polls'
