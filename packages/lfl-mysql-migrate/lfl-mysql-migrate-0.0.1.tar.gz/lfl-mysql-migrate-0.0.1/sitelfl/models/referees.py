from django.db import models


class Referees(models.Model):
    active = models.IntegerField()
    birthday1 = models.DateField(blank=True, null=True)
    contact_id = models.IntegerField()
    debut = models.DateField(blank=True, null=True)
    edited_by_id = models.IntegerField(blank=True, null=True)
    family_name1 = models.CharField(max_length=20, blank=True, null=True)
    first_name1 = models.CharField(max_length=20, blank=True, null=True)
    last_edit_date = models.DateTimeField(blank=True, null=True)
    person_id = models.IntegerField()
    photo11 = models.CharField(max_length=12, blank=True, null=True)
    photo2 = models.CharField(max_length=12, blank=True, null=True)
    photo3 = models.CharField(max_length=12, blank=True, null=True)
    referee_id = models.AutoField(primary_key=True)
    referee_post = models.CharField(max_length=40, blank=True, null=True)
    region_id = models.IntegerField()
    second_name1 = models.CharField(max_length=20, blank=True, null=True)
    unique_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'referees'
