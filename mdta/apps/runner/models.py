from django.db import models
from django.utils.datetime_safe import time


class TestServer(models.Model):
    host = models.TextField()
    remote_user = models.TextField()
    remote_password = models.TextField()
    name = models.TextField(unique=True)



