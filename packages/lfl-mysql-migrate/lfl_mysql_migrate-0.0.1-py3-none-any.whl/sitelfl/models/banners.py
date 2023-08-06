from django.db.models import Model, BigIntegerField, SmallIntegerField, IntegerField, CharField


class Banners(Model):
    active = SmallIntegerField()
    banner_type = SmallIntegerField()
    edited_by_id = IntegerField()
    href = CharField(max_length=256)
    id = BigIntegerField(primary_key=True)
    image = CharField(max_length=256)
    name = CharField(max_length=256)
    overlap = SmallIntegerField()
    padding_top = SmallIntegerField()
    position = IntegerField()
    region_id = IntegerField()
    rotate = CharField(max_length=2)

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        db_table='banners'
        managed = False
        verbose_name = 'Баннеры'
