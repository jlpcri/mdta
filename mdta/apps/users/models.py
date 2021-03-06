from django.db import models
from django.contrib.auth.models import User


class HumanResource(models.Model):
    """
    Link to auth user
    """
    user = models.OneToOneField(User)

    # Last project user working on
    project = models.ForeignKey('projects.Project', null=True, blank=True)
    manager = models.BooleanField(default=False)
    lead = models.BooleanField(default=False)

    def __str__(self):
        return '{0}: {1}'.format(self.user.username, self.project)
