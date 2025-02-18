from django.db import models

class GitHubUserData(models.Model):
    username = models.CharField(max_length=255, unique=True)
    commit_count = models.IntegerField(default=0)
    pull_request_count = models.IntegerField(default=0)
    merged_pull_request_count = models.IntegerField(default=0)
    # Use JSONField if your Django version supports it (Django 3.1+)
    repos = models.JSONField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
