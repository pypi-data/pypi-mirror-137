from django.db.models import Model, AutoField, IntegerField, CharField, TextField, DateTimeField


class Leagues(Model):
    active = IntegerField()
    add_slideshow_tabs = CharField(max_length=255)
    bg_link = CharField(max_length=256)
    contacts = TextField()
    double_logo = CharField(max_length=255, blank=True, null=True)
    edited_by_id = IntegerField(blank=True, null=True)
    eval = TextField(blank=True, null=True)
    header = CharField(max_length=256)
    last_edit_date = DateTimeField(blank=True, null=True)
    league_id = AutoField(primary_key=True)
    logo = CharField(max_length=256, blank=True, null=True)
    middle_link = CharField(max_length=255, blank=True, null=True)
    middle_text = CharField(max_length=255, blank=True, null=True)
    name = CharField(max_length=100, blank=True, null=True)
    name_en = CharField(max_length=255, blank=True, null=True)
    nonphoto = IntegerField()
    parimatch = IntegerField()
    position = IntegerField()
    referees_max = IntegerField()
    region_id = IntegerField()
    right_link = CharField(max_length=255, blank=True, null=True)
    right_logo = CharField(max_length=255, blank=True, null=True)
    script_path = CharField(max_length=1024)
    season_id = IntegerField()
    short_name = CharField(max_length=20, blank=True, null=True)
    show_in_menu = IntegerField()
    show_referee_photo_in_protocols = IntegerField()
    show_shirt_in_protocols = IntegerField()
    show_stadium_photo_in_protocols = IntegerField()
    slideshow_title = CharField(max_length=255)
    social = TextField()
    submenu = IntegerField(blank=True, null=True)
    text = TextField(blank=True, null=True)
    unique_id = CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'leagues'
