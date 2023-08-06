from django.db.models import CharField, IntegerField, Model


class PersonPhotos(Model):
    person_id = IntegerField(primary_key=True)
    image = CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'person_photos'
