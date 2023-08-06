from django.db.models import Model, BigIntegerField, IntegerField, CharField, DateTimeField


class Cards(Model):
    card_id = BigIntegerField(primary_key=True)
    card_type = CharField(max_length=1)
    club_id = IntegerField()
    edited_by_id = BigIntegerField()
    last_edit_date = DateTimeField()
    match_id = IntegerField()
    minute = IntegerField()
    player_id = IntegerField()
    reason = IntegerField()
    referee_id = BigIntegerField()
    take_off = IntegerField()
    tournament_id = BigIntegerField()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        managed = False
        db_table = 'cards'
        verbose_name = 'Карточки игроков в сыгранных матчах: три типа. 1. жёлтая к. 2. Вторая ж.к. 3. красная карточка'
