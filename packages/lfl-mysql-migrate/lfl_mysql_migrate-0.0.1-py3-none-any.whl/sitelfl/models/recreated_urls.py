from django.db.models import Model, BigIntegerField, CharField


class Recreated_urls(Model):
    old_id = BigIntegerField()
    table_name = CharField(max_length=50)
    old_urls = CharField(db_index=True, max_length=767)
    new_urls = CharField(db_index=True, max_length=767, unique=True)

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        db_table = 'recreated_urls'
