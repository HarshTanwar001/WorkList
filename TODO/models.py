from django.db import models


class UserData(models.Model):
    id = models.CharField(primary_key=True, max_length=30)
    tasks = models.JSONField(null=True)
