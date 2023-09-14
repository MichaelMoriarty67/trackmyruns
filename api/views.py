from django.shortcuts import render
from .models import Run, Runner, RunMap
from django.utils import timezone
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.exceptions import ObjectDoesNotExist
import json


# TODO: seems like all routes have some predefined structure for what verbs they accept,
# what params they need to see in the body. Can I make a functional abstraction from this?


# TODO: Errors to handle:
# JSONDEcodeError <-- when data not specified as application/json AND when request body has whitespace and \n
# ie) b'{\n    "run_id": 1,\n    "timestamp": 1694541732082,\n    "longitude": 55.6797,\n    "latitude": -49.7914,\n}'


@csrf_exempt
def runs(request: HttpRequest):
    """GET: Returns a list of all runs
    POST: Creates a new run"""

    # POST Request
    if request.method == "POST":
        try:
            body_json = json.loads(request.body)
            # Remove runner_id & turn into Runner obj that has matching ID
            runner_id = body_json.pop("runner_id")
            runner = Runner.objects.get(
                runner_id=runner_id
            )  # TODO: catch this error when no runner exists with specified id

            new_run = Run(
                **body_json, runner_id=runner
            )  # TODO: may not work if keywords arent all exact, no more no less
            new_run.save()

            new_run_json = new_run.to_json()
            return JsonResponse(new_run_json, safe=False, status=200)
        except (KeyError, ValueError) as e:
            return HttpResponse(
                f"Improper keyword arguments for api/runs/ POST method.\nError Message: {e}",
                status=400,
            )

    # GET Request
    elif request.method == "GET":
        # Fetch QuerySet of all rows in Run table & turn them into JSON.
        queryset_runs = Run.objects.order_by("run_id")
        json_runs = serialize("json", queryset_runs)

        # TODO: queryset --> only a dict of runs (maybe create a helper func?)

        return JsonResponse(json_runs, safe=False, status=200)

    else:
        return HttpResponse(
            "The HTTP Method you're calling on the api/runs/ route is not allowed.",
            status=405,
        )


@csrf_exempt
def run_by_id(request: HttpRequest, run_id: int):
    try:
        # GET Request
        if request.method == "GET":
            # Call get on Runner.objects
            run = Run.objects.get(run_id=run_id)

            # turn run into a JSON serializable obj (dict)
            run_json = run.to_json()

            return JsonResponse(run_json, status=200, safe=False)

        # DELETE Request
        elif request.method == "DELETE":
            run = Run.objects.get(run_id=run_id)
            run.delete()

            return HttpResponse(
                f"Run with ID {run_id} succesfully deleted.", status=200
            )

        else:
            return HttpResponse(
                "The HTTP Method you're calling on the api/runs/:run_id route is not allowed.",
                status=405,
            )
    except ObjectDoesNotExist as e:
        return HttpResponse(
            f"Run with ID {run_id} does not exist.\n Error Message: {e}", status=404
        )
    except json.JSONDecodeError as e:
        return HttpResponse(
            f"Bad request due to improper JSON formatting.\n Error Message: {e}",
            status=400,
        )


@csrf_exempt
def run_map_by_id(request: HttpRequest, run_id: int):
    try:
        # GET Request
        if request.method == "GET":
            run = Run.objects.get(run_id=run_id)

            run_coords = RunMap.objects.filter(
                run_id=run
            ).values()  # TODO: How can I get all values from ValueQuerySet instead of creating copy?

            run_map_json = []
            for run_map in run_coords:
                run_map_json.append(run_map)

            return JsonResponse(run_map_json, safe=False, status=200)

        # POST Request
        elif request.method == "POST":
            body_json = json.loads(request.body)

            # Fetch Run instance using run_id
            run = Run.objects.get(run_id=run_id)

            # Iterate over each RunMap in json data
            if isinstance(body_json, list):
                map_array = []

                for map_dict in body_json:
                    map_dict["run_id"] = run
                    map = RunMap(**map_dict)
                    map.save()

                    map_array.append(map.to_json())

                return JsonResponse(map_array, safe=False, status=200)

            else:
                body_json["run_id"] = run
                map = RunMap(**body_json)
                map.save()

                return JsonResponse(map.to_json(), safe=False, status=200)

        else:
            return HttpResponse(
                "The HTTP Method you're calling on the api/runs/:run_id/map route is not allowed.",
                status=405,
            )
    except ObjectDoesNotExist as e:
        return HttpResponse(
            f"Run with ID {run_id} does not exist.\n Error Message: {e}", status=404
        )
    except json.JSONDecodeError as e:
        return HttpResponse(
            f"Bad request due to improper JSON formatting.\n Error Message: {e}",
            status=400,
        )


@csrf_exempt
def user(request: HttpRequest):
    """POST: Create a new user."""

    try:
        if request.method == "POST":
            body_json = json.loads(request.body)

            new_user = Runner(**body_json)
            new_user.save()

            new_user_json = new_user.to_json()
            return JsonResponse(new_user_json, safe=False, status=200)

        else:
            return HttpResponse(
                "The HTTP Method you're calling on the api/user/ route is not allowed.",
                status=405,
            )

    except KeyError as e:
        return HttpResponse(
            f"Improper keyword arguments for api/user/ POST method.\nError Message: {e}",
            status=400,
        )
    except json.JSONDecodeError as e:
        return HttpResponse(
            f"Bad request due to improper JSON formatting.\n Error Message: {e}",
            status=400,
        )


@csrf_exempt
def user_by_id(request: HttpRequest, user_id: int):
    try:
        # GET Request
        if request.method == "GET":
            user = Runner.objects.get(runner_id=user_id)

            return JsonResponse(user.to_json(), safe=False, status=200)

        # PATCH Request
        elif request.method == "PATCH":
            body_json = json.loads(request.body)

            user = Runner.objects.get(runner_id=user_id)

            for key in body_json.keys():
                if hasattr(user, f"{key}"):
                    setattr(user, f"{key}", body_json[f"{key}"])

                else:
                    return HttpResponse(
                        f"Error: Requesting to update attributes that do not exist on user with ID {user_id}.",
                        status=404,
                    )

            user.save()

            return JsonResponse(user.to_json(), safe=False, status=200)

        else:
            return HttpResponse(
                "The HTTP Method you're calling on the api/user/:user_id route is not allowed.",
                status=405,
            )
    except (
        ObjectDoesNotExist
    ) as e:  # TODO: watch out if exposing a user_id or this info publically is ok? Maybe should return an unauthorized error instead.
        return HttpResponse(
            f"User with ID {user_id} does not exist.\n Error Message: {e}", status=404
        )
    except json.JSONDecodeError as e:
        return HttpResponse(
            f"Bad request due to improper JSON formatting.\n Error Message: {e}",
            status=400,
        )


@csrf_exempt
def runs_by_user_id(
    request: HttpRequest, user_id: int
):  # TODO: can this be consolidated into user_by_id by catching /runs route?
    # GET Request
    try:
        user = Runner.objects.get(runner_id=user_id)
        user_runs = Run.objects.filter(runner_id=user).values()

        user_runs_json = []
        for run in user_runs:
            user_runs_json.append(run)

        return JsonResponse(user_runs_json, safe=False, status=200)

    except (
        ObjectDoesNotExist
    ) as e:  # TODO: watch out if exposing a user_id or this info publically is ok? Maybe should return an unauthorized error instead.
        return HttpResponse(
            f"User with ID {user_id} does not exist.\n Error Message: {e}", status=404
        )
