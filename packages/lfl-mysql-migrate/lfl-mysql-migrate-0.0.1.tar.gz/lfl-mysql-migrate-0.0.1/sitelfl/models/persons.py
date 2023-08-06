from django.db.models import Model, AutoField, IntegerField, CharField, DateField, DateTimeField, TextField
from isc_common.datetime import DateToStr


class Persons(Model):
    active = IntegerField()
    admin_comment = TextField(blank=True, null=True)
    archive = IntegerField()
    birthday = DateField(blank=True, null=True)
    created_by = IntegerField()
    edited_by_id = IntegerField(blank=True, null=True)
    email = CharField(max_length=255)
    email2 = CharField(max_length=255)
    family_name = CharField(max_length=20, blank=True, null=True)
    family_name_en = CharField(max_length=255, blank=True, null=True)
    first_name = CharField(max_length=20, blank=True, null=True)
    first_name_en = CharField(max_length=255, blank=True, null=True)
    last_edit_date = DateTimeField(blank=True, null=True)
    person_id = AutoField(primary_key=True)
    photo = CharField(max_length=255)
    region_id = IntegerField()
    second_name = CharField(max_length=20, blank=True, null=True)
    second_name_en = CharField(max_length=255, blank=True, null=True)
    telephone = CharField(max_length=40)
    telephone2 = CharField(max_length=40)

    def __str__(self):
        return f"person_id: {self.person_id} {self.family_name} {self.first_name} {self.second_name} {DateToStr(self.birthday)} г.р. region_id: {self.region_id}"

    class Meta:
        managed = False
        db_table = 'persons'
