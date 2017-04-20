from django.db import models
from django.utils.datetime_safe import time


class TestServer(models.Model):
    host = models.TextField()
    remote_user = models.TextField()
    remote_password = models.TextField()
    name = models.TextField(unique=True)


def hatitfile_location(instance, filename):
    return "{0}_{1}".format(str(time.time()).replace('.', ''), filename)


class HatitFiles(models.Model):
    filename = models.TextField()
    upload = models.FileField(upload_to=hatitfile_location)
    suiteID = models.TextField()


