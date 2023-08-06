from django.db import models


class Fines(models.Model):
    active = models.IntegerField()
    club_id = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    deleting = models.IntegerField()
    edited_by_id = models.IntegerField(blank=True, null=True)
    fine_id = models.AutoField(primary_key=True)
    kdk_id = models.IntegerField()
    last_edit_date = models.DateTimeField(blank=True, null=True)
    payment = models.IntegerField()
    remove_restore_date = models.DateField(blank=True, null=True)
    sum = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'fines'
