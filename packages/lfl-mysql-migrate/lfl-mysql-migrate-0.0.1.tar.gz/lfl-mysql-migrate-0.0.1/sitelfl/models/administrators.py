from django.db.models import BigIntegerField, CharField, IntegerField, SmallIntegerField, TextField, DateTimeField, Model


class Administrators(Model):
    access = CharField(max_length=255, default='')  # *
    active = SmallIntegerField(default=1)  # *
    admin_id = BigIntegerField(primary_key=True)  # *
    admin_post = CharField(max_length=20, null=True, blank=True)  # *
    admin_weight = IntegerField(default=0)  # *
    all_news_access = IntegerField(default=0)  # *
    clubs = TextField()  # *
    contact_id = IntegerField(default=0)  # *
    edited_by_id = IntegerField()  # *
    kdk_fine_deleting = SmallIntegerField(default=0)  # *
    last_edit_date = DateTimeField(null=True, blank=True)  # *
    last_visit = DateTimeField(null=True, blank=True)  # *
    login = CharField(max_length=20, null=True, blank=True)  # *
    name = CharField(max_length=30, null=True, blank=True)  # *
    password = CharField(max_length=255)  # *
    person_editing = SmallIntegerField(default=0)
    photo = CharField(max_length=12)
    public_access = SmallIntegerField(default=0)
    register_date = DateTimeField(null=True, blank=True)  # *
    send_email = SmallIntegerField(default=1)
    transfer_right = SmallIntegerField(default=1)
    unique_id = CharField(max_length=50, unique=True)

    def __str__(self):
        return f'ID:{self.admin_id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        managed = False
        db_table = 'administrators'
        verbose_name = 'Администраторы'
