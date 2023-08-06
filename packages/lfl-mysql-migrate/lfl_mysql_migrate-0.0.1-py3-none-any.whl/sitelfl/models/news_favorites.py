from django.db import models


class NewsFavorites(models.Model):
    admin_id = models.IntegerField(primary_key=True)
    id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'news_favorites'
        unique_together = (('admin_id', 'id'),)
