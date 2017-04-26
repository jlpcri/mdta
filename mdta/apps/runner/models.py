from django.db import models
from django.utils.datetime_safe import time


class TestServer(models.Model):
    server = models.TextField()
    name = models.TextField(unique=True)




