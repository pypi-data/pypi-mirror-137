from django.db.models import IntegerField, CharField, Model, AutoField, DateField


class ClubHistories(Model):
    active = IntegerField()
    club_id = IntegerField()
    edited_by_id = IntegerField()
    end_date = DateField(blank=True, null=True)
    name = CharField(max_length=255)
    name_id = AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'club_histories'
