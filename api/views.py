from django.shortcuts import render
from .models import Run, Runner, RunMap
from django.utils import timezone
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
import json


# TODO: seems like all routes have some predefined structure for what verbs they accept,
# what params they need to see in the body. Can I make a functional abstraction from this?


# TODO: Errors to handle:
# JSONDEcodeError <-- when data not specified as application/json


@csrf_exempt
def runs(request: HttpRequest):
    """GET: Returns a list of all runs
    POST: Creates a new run"""

    if request.method == "POST":
        # POST Response
        try:
            json_data = json.loads(request.body)

            # Remove runner_id & turn into Runner obj that has matching ID
            runner_id = json_data.pop("runner_id")
            breakpoint()

            runner = Runner.objects.get(
                runner_id=runner_id
            )  # TODO: catch this error when no runner exists with specified id

            new_run = Run(
                **json_data, runner_id=runner
            )  # TODO: may not work if keywords arent all exact, no more no less
            new_run.save()

            new_run_json = new_run.to_json()
            return JsonResponse(new_run_json, safe=False, status=200)
        except (KeyError, ValueError) as e:
            return HttpResponse(
                f"Improper keyword arguments for api/runs/ POST method.\nError Message: {e}",
                status=400,
            )

    elif request.method == "GET":
        # GET Response
        # Fetch QuerySet of all rows in Run table & turn them into JSON.
        queryset_runs = Run.objects.order_by("run_id")
        json_runs = serialize("json", queryset_runs)

        return JsonResponse(json_runs, safe=False, status=200)

    else:
        pass
        # TODO: add in logic to send back bad error codes if not using GET / POST


def run_by_id(request: HttpRequest, run_id: int):
    # GET Request
    # PUT Request
    # DELETE Request

    response = f"Here are the details for the run with id {run_id}"
    return HttpResponse(response)


@csrf_exempt
def user(request: HttpRequest):
    """POST: Create a new user."""

    try:
        if request.method == "POST":
            breakpoint()
            json_data = json.loads(request.body)

            new_user = Runner(**json_data)
            new_user.save()

            new_user_json = new_user.to_json()
            return JsonResponse(new_user_json, safe=False, status=200)

        else:
            return HttpResponse(
                "The HTTP Method you're calling on the api/user/ route is not allowed.",
                status=405,
            )

    except (KeyError, ValueError) as e:
        return HttpResponse(
            f"Improper keyword arguments for api/user/ POST method.\nError Message: {e}",
            status=400,
        )


def user_by_id(request: HttpRequest, user_id: int):
    # GET Request
    # PUT Request

    pass


def runs_by_user_id(
    request: HttpRequest, user_id: int
):  # TODO: can this be consolidated into user_by_id by catching /runs route?
    # GET Request

    pass
