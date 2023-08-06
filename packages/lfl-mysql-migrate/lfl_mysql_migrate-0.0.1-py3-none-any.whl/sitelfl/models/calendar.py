from django.db.models import Model, BigIntegerField, IntegerField, SmallIntegerField, CharField, DateTimeField, TextField, BinaryField


class Calendar(Model):
    away_formation = IntegerField()
    away_id = IntegerField()
    away_points = IntegerField()
    away_score = CharField(max_length=2)
    away_shirt = CharField(max_length=255)
    away_shirt_keeper = CharField(max_length=255)
    checked = SmallIntegerField()
    comment = TextField()
    division_id = IntegerField()
    edited_by_id = IntegerField()
    gallery_link = CharField(max_length=255)
    home_formation = IntegerField()
    home_id = IntegerField()
    home_points = IntegerField()
    home_score = CharField(max_length=255)
    home_shirt = CharField(max_length=255)
    home_shirt_keeper = CharField(max_length=255)
    in_archive = SmallIntegerField()
    last_edit_date = DateTimeField()
    league_id = IntegerField()
    match_cast = CharField(max_length=50)
    match_date_time = DateTimeField()
    match_id = BigIntegerField(primary_key=True)
    match_number = IntegerField()
    next_match = IntegerField()
    note = CharField(max_length=200)
    protocol = SmallIntegerField()
    referee_id = IntegerField()
    season_id = SmallIntegerField()
    show_stats = SmallIntegerField()
    stadium_id = IntegerField()
    technical_defeat = BinaryField()
    tour = SmallIntegerField()
    tournament_id = IntegerField()
    show_empty_cells = SmallIntegerField()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        managed = False
        db_table = 'calendar'
        verbose_name = 'Календарь матчей турнира'
