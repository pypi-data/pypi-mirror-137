from django.db import models


class Players(models.Model):
    active = models.IntegerField()
    amplua = models.IntegerField()
    birthday1 = models.DateField(blank=True, null=True)
    blocked = models.IntegerField()
    club_id_now = models.IntegerField()
    debut = models.DateField(blank=True, null=True)
    delayed_lockout = models.IntegerField()
    delayed_lockout_date = models.DateField(blank=True, null=True)
    delayed_lockout_reason = models.CharField(max_length=255)
    disqualification = models.IntegerField()
    edited_by_id = models.IntegerField(blank=True, null=True)
    family_name1 = models.CharField(max_length=20, blank=True, null=True)
    first_name1 = models.CharField(max_length=20, blank=True, null=True)
    height = models.IntegerField()
    included = models.DateField(blank=True, null=True)
    last_edit_date = models.DateTimeField(blank=True, null=True)
    lockout = models.IntegerField()
    lockout_reason = models.CharField(max_length=80, blank=True, null=True)
    medical_admission_date = models.DateField(blank=True, null=True)
    medical_lockout = models.IntegerField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    old_base_id = models.CharField(max_length=10)
    person_id = models.IntegerField()
    photo11 = models.CharField(max_length=12, blank=True, null=True)
    photo2 = models.CharField(max_length=12, blank=True, null=True)
    photo3 = models.CharField(max_length=12, blank=True, null=True)
    player_id = models.AutoField(primary_key=True)
    region_id = models.IntegerField()
    second_name1 = models.CharField(max_length=20, blank=True, null=True)
    shadow = models.IntegerField()
    size_of_photo = models.IntegerField()
    unique_id = models.CharField(max_length=50, blank=True, null=True)
    weight = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'players'
