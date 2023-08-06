from django.db.models import Model, AutoField, IntegerField, CharField


class ClubContacts(Model):
    active = IntegerField()
    club_id = IntegerField()
    contact_id = AutoField(primary_key=True)
    edited_by_id = IntegerField()
    leader = IntegerField()
    person_id = IntegerField()
    post = CharField(max_length=255)
    priority = IntegerField()

    class Meta:
        managed = False
        db_table = 'club_contacts'
