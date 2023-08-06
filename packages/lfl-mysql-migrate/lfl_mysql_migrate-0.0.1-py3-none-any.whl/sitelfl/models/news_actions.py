from django.db import models
from django.db.models import BigIntegerField


class NewsActions(models.Model):
    dt = models.DateTimeField()
    from_data = models.TextField(blank=True, null=True)
    from_tag = models.TextField(blank=True, null=True)
    id = BigIntegerField(primary_key=True)
    news_id = models.IntegerField()
    to_data = models.TextField(blank=True, null=True)
    to_tag = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=7)
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'news_actions'
