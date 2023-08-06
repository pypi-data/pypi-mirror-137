from django.db import models


class PollAnswers(models.Model):
    active = models.IntegerField()
    answer_id = models.AutoField(primary_key=True)
    edited_by_id = models.IntegerField()
    name = models.CharField(max_length=255)
    poll_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'poll_answers'
