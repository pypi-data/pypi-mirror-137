from django.db.models import Model, IntegerField


class StadiumRating(Model):
    stadium_id = IntegerField(primary_key=True)
    league_id = IntegerField()
    rating = IntegerField()

    class Meta:
        managed = False
        db_table = 'stadium_rating'
        unique_together = (('stadium_id', 'league_id'),)
