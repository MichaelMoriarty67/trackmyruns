from django.db import models
from django.utils import timezone

# Create your models here.


class Runner(models.Model):
    runner_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    longest_run = models.ForeignKey(
        "Run", on_delete=models.PROTECT
    )  # using lazy ref to run because it's not defined yet
    # TODO: I should create a custom on_delete function that sets longest_run field to the runners next longest run if longest is deleted
    total_kms = models.FloatField(default=0)
    total_time = models.IntegerField(default=0)


class Run(models.Model):
    run_id = models.AutoField(primary_key=True)
    runner_id = models.ForeignKey(
        Runner, on_delete=models.CASCADE
    )  # all runs are deleted when associated runner is deleted
    title = models.CharField(default="My Epic Run!", max_length=250)
    start_time = models.BigIntegerField(default=timezone.now().timestamp())
    date_pub = models.DateTimeField(verbose_name="publish date")
    total_kms = models.FloatField(default=0, verbose_name="distance in kms")
    total_time = models.IntegerField(default=0, verbose_name="time in seconds")

    def __str__(self):
        return f"{self.date_pub.year}/{self.date_pub.month}/{self.date_pub.day} | {self.duration_kms}km | {self.duration_sec / 60} min"


class RunMap(models.Model):
    run_id = models.ForeignKey(
        Run, on_delete=models.CASCADE
    )  # all co-ord time entries are deleted when associated run is deleted
    timestamp = models.BigIntegerField(
        default=0
    )  # if no time entered, set to 0 to represent a null stamp
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
