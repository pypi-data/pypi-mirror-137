from django.db import models


class PollVotes(models.Model):
    answer_id = models.IntegerField()
    author = models.CharField(max_length=255)
    poll_id = models.IntegerField()
    time = models.DateTimeField()
    vote_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'poll_votes'
