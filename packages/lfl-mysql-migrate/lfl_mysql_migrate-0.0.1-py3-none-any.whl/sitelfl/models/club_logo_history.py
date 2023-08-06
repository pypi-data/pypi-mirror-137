from django.db.models import IntegerField, CharField, DateTimeField, Model


class ClubLogoHistory(Model):
    club_id = IntegerField()
    logo = CharField(max_length=30, blank=True, null=True)
    dt = DateTimeField()
    filename = CharField(max_length=255, blank=True, null=True)
    admin_id = IntegerField()

    class Meta:
        managed = False
        db_table = 'club_logo_history'
