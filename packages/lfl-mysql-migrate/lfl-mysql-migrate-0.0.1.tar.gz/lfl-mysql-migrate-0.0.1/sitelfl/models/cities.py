from django.db.models import Model, IntegerField, CharField


class Cities(Model):
    city_id = IntegerField(primary_key=True)
    city_region_id = IntegerField()
    name = CharField(max_length=255)
    logo = CharField(max_length=255)
    geo = CharField(max_length=255)

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        managed = False
        verbose_name = 'Города'
        db_table = "cities~"
