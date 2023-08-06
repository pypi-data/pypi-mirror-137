from django.db import models


class NewsQuantityByUrl(models.Model):
    id = None
    url = models.CharField(max_length=1024)
    quantity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news_quantity_by_url'
