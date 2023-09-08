from django.shortcuts import render
from .models import Run, Runner, RunMap
from django.utils import timezone

# Create your views here.
from django.http import HttpResponse


def index(request):
    runs = Run.objects.order_by("-date_pub")
    output = [r.duration_kms for r in runs]

    return HttpResponse(f"Your longest runs: {output}")


def runs_by_id(request, run_id):
    response = f"Here are the details for the run with id {run_id}"
    return HttpResponse(response)


def create_run(request, run_id):
    new_run = Run(date_pub=timezone.now(), duration_kms=69.420, duration_sec=run_id)
    new_run.save()

    return HttpResponse(f"You're creating a run: {new_run}")
