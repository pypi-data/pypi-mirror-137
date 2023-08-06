from django.db.models import Model, AutoField, CharField, IntegerField


class Shirts(Model):
    active = IntegerField()
    edited_by_id = IntegerField()
    name = CharField(max_length=255)
    shirt_id = AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'shirts'
