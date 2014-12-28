from django.db import models

# Create your models here.

class ShortenUrls(models.Model):

    url = models.CharField(max_length=255)
    short = models.CharField(max_length=20)
    created = models.DateField(auto_now_add=True)

    no_clicks = models.BigIntegerField()

    def __unicode__(self):
        return '{0}'.format(self.short)
