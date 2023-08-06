from django.db.models import Model, IntegerField, CharField, AutoField, TextField


class Stadiums(Model):
    stadium_id = AutoField(primary_key=True)
    region_id = IntegerField()
    name = CharField(max_length=100, blank=True, null=True)
    address = CharField(max_length=200, blank=True, null=True)
    logo = CharField(max_length=12, blank=True, null=True)
    plan = CharField(max_length=12, blank=True, null=True)
    photo = CharField(max_length=30, blank=True, null=True)
    active = CharField(max_length=1)
    description = TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stadiums'
