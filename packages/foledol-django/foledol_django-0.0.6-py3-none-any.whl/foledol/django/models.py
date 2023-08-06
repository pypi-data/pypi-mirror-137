from django.contrib.auth.models import User
from django.db import models


class Log(models.Model):
    user: User = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='actor')
    ref = models.CharField(max_length=64, default='')
    model = models.CharField(max_length=64, default='')
    date = models.DateTimeField(auto_now_add=True, editable=True, null=True, blank=True)
    diff = models.TextField(default='')
    action = models.CharField(max_length=64, default='')
    transaction = models.CharField(max_length=64, default='', null=True)

    def __str__(self):
        return str(self.id)

    def author(self):
        return self.user.username if self.user else '(admin)'


class LogItem(models.Model):
    log = models.ForeignKey(Log, on_delete=models.DO_NOTHING, null=True, related_name='items')
    key = models.CharField(max_length=128, default='')
    old = models.CharField(max_length=128, default='', null=True)
    new = models.CharField(max_length=128, default='', null=True)

    def __str__(self):
        return str(self.id)
