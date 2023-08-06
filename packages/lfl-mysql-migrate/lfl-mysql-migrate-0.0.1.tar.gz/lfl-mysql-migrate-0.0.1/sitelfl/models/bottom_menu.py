from django.db.models import Model, BigIntegerField, IntegerField, CharField, SmallIntegerField


class Bottom_menu(Model):
    id = BigIntegerField(primary_key=True)
    parent_id = IntegerField()
    position = IntegerField()
    name = CharField(max_length=255)
    url = CharField(max_length=255)
    type = SmallIntegerField()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        managed = False
        db_table = 'bottom_menu'
        verbose_name = 'Правое вертикальное меню МОСТ'
