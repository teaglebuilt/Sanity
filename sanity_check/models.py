from django.db import models
from django.contrib.auth.models import User


class Site(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=256)
    last_response_code = models.CharField(max_length=8, blank=True, null=True)
    last_check = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.url)

class Check(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    response_code = models.CharField(max_length=8)

    def __str__(self):
        return "url: {}, code: {}".format(self.site.url, self.response_code)

        