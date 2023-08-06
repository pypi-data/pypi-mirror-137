from django.db.models import Model, BigIntegerField, IntegerField, DateTimeField


class Assists(Model):
    assist_id = BigIntegerField(primary_key=True)
    club_id = IntegerField()
    edited_by_id = IntegerField()
    last_edit_date = DateTimeField()
    match_id = IntegerField()
    player_id = IntegerField()
    tournament_id = IntegerField()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        managed = False
        db_table = 'assists'
        verbose_name = 'Голевые пасы в сыгранных матчах. Другое название игрока: ассистент.'
