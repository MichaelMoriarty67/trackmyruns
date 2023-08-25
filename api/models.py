from django.db import models

# Create your models here.


class Run(models.Model):
    date_pub = models.DateTimeField("publish date")
    duration_kms = models.FloatField(default=0)
    duration_sec = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.date_pub.year}/{self.date_pub.month}/{self.date_pub.day} | {self.duration_kms}km | {self.duration_sec / 60} min"
