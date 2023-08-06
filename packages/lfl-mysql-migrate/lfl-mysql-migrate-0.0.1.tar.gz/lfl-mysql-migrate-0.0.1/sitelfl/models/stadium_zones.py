from django.db.models import Model, IntegerField


class StadiumZones(Model):
    stadium_id = IntegerField(primary_key=True)
    league_id = IntegerField()

    class Meta:
        managed = False
        db_table = 'stadium_zones'
        unique_together = (('stadium_id', 'league_id'),)
