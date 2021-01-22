from django.db import models

class User(models.Model):
    number          = models.CharField(max_length=30, null=True)
    name            = models.CharField(max_length=30, null=True)
    email           = models.CharField(max_length=100, null=True)
    password        = models.CharField(max_length=300, null=True)
    social_id = models.CharField(max_length=100, null=True)

    class Meta :
        db_table = 'users'
