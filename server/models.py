
import uuid
from django.db import models

DATAMODE = (('A', 'Active'), ('I', 'Inactive'), ('D', 'Deleted'))
HTTP_METHOD = (('POST', 'POST'), ('GET', 'GET'), ('PUT', 'PUT'), ('DELETE', 'DELETE'))


class Account(models.Model):
    email_id = models.EmailField(unique=True)
    account_id = models.CharField(max_length=255, unique=True)
    account_name = models.CharField(max_length=255)
    app_secert_token = models.UUIDField(null=True, blank=True, unique=True)
    website = models.URLField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=128, default="A", choices=DATAMODE)

    def save(self, *args, **kwargs):
        super(Account, self).save(*args, **kwargs)
        if not(self.app_secert_token):
            self.app_secert_token = uuid.uuid4()
            super(Account, self).save()

    def __str__(self):
        return "{0}".format(self.account_id)


class Destination(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    destination = models.URLField()
    http_method = models.CharField(max_length=128, choices=HTTP_METHOD, default="POST")
    headers = models.JSONField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=128, default="A", choices=DATAMODE)

    def __str__(self):
        return "{0}".format(self.account.account_id)