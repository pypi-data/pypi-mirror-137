from django.db.models import Model, IntegerField, CharField


class PersonClubPhotos(Model):
    club_id = IntegerField()
    is_main = IntegerField()
    num = IntegerField()
    person_id = IntegerField()
    photo = CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'person_club_photos'
