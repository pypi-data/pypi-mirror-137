from django.db.models import Model, AutoField, CharField, IntegerField


class ShirtImages(Model):
    image_id = AutoField(primary_key=True)
    name = CharField(max_length=255)
    value = CharField(max_length=255)
    position = IntegerField()
    shirt_id = IntegerField()
    active = IntegerField()
    edited_by_id = IntegerField()

    class Meta:
        managed = False
        db_table = 'shirt_images'
