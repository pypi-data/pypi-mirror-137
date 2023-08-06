from django.db.models import Model, AutoField, CharField, DateField, IntegerField, DateTimeField


class Seasons(Model):
    active = IntegerField()
    comment = CharField(max_length=128, blank=True, null=True)
    edited_by_id = IntegerField(blank=True, null=True)
    end_date = DateField(blank=True, null=True)
    last_edit_date = DateTimeField(blank=True, null=True)
    name = CharField(max_length=100, blank=True, null=True)
    season_id = AutoField(primary_key=True)
    start_date = DateField(blank=True, null=True)
    unique_id = CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seasons'
