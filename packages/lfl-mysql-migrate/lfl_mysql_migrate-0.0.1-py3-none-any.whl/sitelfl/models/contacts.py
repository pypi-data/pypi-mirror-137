from django.db.models import Model, AutoField, IntegerField, CharField, DateTimeField


class Contacts(Model):
    club_id = IntegerField(blank=True, null=True)
    contact_id = AutoField(primary_key=True)
    edited_by_id = IntegerField(blank=True, null=True)
    email = CharField(max_length=50, blank=True, null=True)
    family_name = CharField(max_length=20, blank=True, null=True)
    first_name = CharField(max_length=20, blank=True, null=True)
    last_edit_date = DateTimeField(blank=True, null=True)
    mobile = CharField(max_length=20, blank=True, null=True)
    second_name = CharField(max_length=20, blank=True, null=True)
    telephone = CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contacts'
