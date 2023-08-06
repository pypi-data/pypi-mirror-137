from django.db import models


class Formation(models.Model):
    formation_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    priority = models.CharField(max_length=3)
    formation = models.CharField(max_length=255)
    number_of_players = models.CharField(max_length=3)
    edited_by_id = models.IntegerField()
    active = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'formation'
