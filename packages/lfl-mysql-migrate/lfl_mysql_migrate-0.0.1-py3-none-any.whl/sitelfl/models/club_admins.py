from django.db.models import Model, AutoField, IntegerField


class ClubAdmins(Model):
    club_admin_id = AutoField(primary_key=True)
    club_id = IntegerField()
    user_id = IntegerField()
    active = IntegerField()
    edited_by_id = IntegerField()

    class Meta:
        managed = False
        db_table = 'club_admins'
        unique_together = (('club_id', 'user_id'),)
