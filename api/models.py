from django.db import models
from django.utils import timezone
from .utils import change_in_time_and_kms

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

    def save(self, *args, **kwargs):
        # Adjustments before saving
        self.total_kms = round(self.total_kms, 4)

        # Call save() on base class
        super(Run, self).save(*args, **kwargs)

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

    def add_run_map(self, new_map):
        """Evaluate and add the change in distance (kms) and time (s) to a Run's total_kms
        and total_time from a single RunMap."""
        diff_kms = 0
        diff_time = 0

        curr_timestamp = new_map.timestamp
        prev_map = (
            RunMap.objects.filter(run_id=self.run_id)
            .filter(timestamp__lte=curr_timestamp)
            .exclude(id=new_map.id)
            .order_by("-timestamp")
            .first()
        )
        breakpoint()

        if prev_map:
            diff_kms, diff_time = change_in_time_and_kms(new_map, prev_map)

        self.total_time += diff_time
        self.total_kms += diff_kms

        self.runner_id.total_time += diff_time  # Update Runner totals
        self.runner_id.total_kms += diff_kms

        self.save()

    def add_multiple_run_maps(self, new_run_maps: list):
        """Evaluate and add the change in distance (kms) and time (s) to a Run's total_kms
        and total_time across multiple RunMaps."""
        diff_time: int = 0
        diff_kms: float = 0.00

        total_time: int = 0
        total_kms: float = 0.00

        for new_map in new_run_maps:
            curr_timestamp = new_map.timestamp

            prev_map = (
                RunMap.objects.filter(run_id=self.run_id)
                .filter(timestamp__lte=curr_timestamp)
                .exclude(id=new_map.id)
                .order_by("-timestamp")
                .first()
            )

            if prev_map:
                diff_kms, diff_time = change_in_time_and_kms(new_map, prev_map)

            total_kms += diff_kms
            total_time += diff_time

        self.total_time += total_time
        self.total_kms += total_kms

        self.runner_id.total_time += total_time  # Update Runner totals
        self.runner_id.total_kms += total_kms

        self.save()

    def save(self, *args, **kwargs):
        # Adjustments before saving
        self.total_kms = round(self.total_kms, 4)

        # Call save() on base class
        super(Run, self).save(*args, **kwargs)

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
        return f"ID: {self.run_id} | {self.date_pub.year}/{self.date_pub.month}/{self.date_pub.day} | {self.total_kms}km | {self.total_time / 60} min"


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
