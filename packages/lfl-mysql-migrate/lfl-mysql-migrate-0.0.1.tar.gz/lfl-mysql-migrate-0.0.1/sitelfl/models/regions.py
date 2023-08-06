from django.db.models import Model, AutoField, IntegerField, CharField, TextField, DateTimeField


class Regions(Model):
    active = IntegerField()
    color = IntegerField()
    contacts = TextField()
    current_season_id = IntegerField()
    double_logo = CharField(max_length=255, blank=True, null=True)
    edited_by_id = IntegerField(blank=True, null=True)
    header = CharField(max_length=1024)
    interregion_id = IntegerField()
    last_edit_date = DateTimeField(blank=True, null=True)
    leagues_menu = IntegerField()
    logo = CharField(max_length=255, blank=True, null=True)
    middle_link = CharField(max_length=255, blank=True, null=True)
    middle_text = CharField(max_length=255, blank=True, null=True)
    name = CharField(max_length=100, blank=True, null=True)
    name_en = CharField(max_length=255, blank=True, null=True)
    parimatch = IntegerField()
    priority = IntegerField(blank=True, null=True)
    region_id = AutoField(primary_key=True)
    region_zone_id = IntegerField()
    right_link = CharField(max_length=255, blank=True, null=True)
    right_logo = CharField(max_length=255, blank=True, null=True)
    select_division = IntegerField(blank=True, null=True)
    submenu = IntegerField(blank=True, null=True)
    text = TextField(blank=True, null=True)
    unique_id = CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'regions'
