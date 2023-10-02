from django.db import models
from django.utils import timezone

# Create your models here.


class Runner(models.Model):
    runner_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    longest_run = models.ForeignKey(
        "Run", on_delete=models.SET_NULL, null=True
    )  # using lazy ref because Run class not defined yet
    # TODO: I should create a custom on_delete function that sets longest_run field to the runners next longest run if longest is deleted
    total_kms = models.FloatField(default=0)
    total_time = models.IntegerField(default=0)
    runner_firebase_uid = models.CharField(max_length=128, default="N/A")

    def to_json(self) -> dict:
        runner_json = {
            "runner_id": self.runner_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "longest_run": self.longest_run,
            "total_kms": self.total_kms,
            "total_time": self.total_time,
        }

        return runner_json


class Run(models.Model):
    run_id = models.AutoField(primary_key=True)
    runner_id = models.ForeignKey(
        Runner, on_delete=models.CASCADE, name="runner_id"
    )  # all runs are deleted when associated runner is deleted
    title = models.CharField(default="My Epic Run!", max_length=250)
    start_time = models.BigIntegerField(default=timezone.now().timestamp())
    date_pub = models.DateTimeField(verbose_name="publish date")
    total_kms = models.FloatField(default=0, verbose_name="distance in kms")
    total_time = models.IntegerField(default=0, verbose_name="time in seconds")

    def to_json(self) -> dict:  # TODO
        run_json = {
            "run_id": self.run_id,
            "runner_id": self.runner_id.runner_id,
            "title": self.title,
            "start_time": self.start_time,
            "date_pub": str(self.date_pub),
            "total_kms": self.total_kms,
            "total_time": self.total_time,
        }

        return run_json

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

    def to_json(self):
        map_json = {
            "run_map_id": self.id,
            "run_id": self.run_id.run_id,
            "timestamp": self.timestamp,
            "longitude": self.longitude,
            "latitude": self.latitude,
        }

        return map_json
