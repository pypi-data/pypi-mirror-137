from django.db import models


class Divisions(models.Model):
    active = models.IntegerField()
    completed = models.IntegerField()
    disqualification_condition = models.IntegerField()
    division_id = models.AutoField(primary_key=True)
    edited_by_id = models.IntegerField(blank=True, null=True)
    last_edit_date = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    number_of_rounds = models.IntegerField()
    page_height = models.IntegerField(blank=True, null=True)
    region_id = models.IntegerField()
    scheme = models.CharField(max_length=255)
    show_news = models.IntegerField()
    top_text = models.TextField()
    unique_id = models.CharField(max_length=50, blank=True, null=True)
    zone_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'divisions'
