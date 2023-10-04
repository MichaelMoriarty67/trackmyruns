from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.core.exceptions import ObjectDoesNotExist

import os
import json
import firebase_admin
from firebase_admin import credentials, auth

from app.settings import env
from .models import Run, Runner, RunMap
from .utils import timestamp_to_tz_date


# TODO: seems like all routes have some predefined structure for what verbs they accept,
# what params they need to see in the body. Can I make a functional abstraction from this?


# TODO: Errors to handle:
# JSONDEcodeError <-- when data not specified as application/json AND when request body has whitespace and \n
# ie) b'{\n    "run_id": 1,\n    "timestamp": 1694541732082,\n    "longitude": 55.6797,\n    "latitude": -49.7914,\n}'
cred_file_path = os.getcwd() + "/FirebaseServerKey.json"
cred = credentials.Certificate(cred_file_path)
default_app = firebase_admin.initialize_app(cred)


class RESTError(Exception):
    ERROR_MAP = {
        "KeyError": {"message": "Invalid arguments", "status": 400},
        "ValueError": {"message": "Invalid arguments", "status": 400},
        "TypeError": {"message": "Invalid arguments", "status": 400},
        "InvalidIdTokenError": {"message": "Invalid ID Token", "status": 400},
        "ExpiredIdTokenError": {"message": "Expired ID Token", "status": 401},
        "RevokedIdTokenError": {"message": "Invalid ID Token", "status": 401},
        "CertificateFetchError": {
            "message": "Server Error during ID Token validation.",
            "status": 500,
        },
        "FirebaseError": {
            "message": "Server Error.",
            "status": 500,
        },
        "UserDisabledError": {"message": "Invalid ID Token", "status": 401},
        "JSONDecodeError": {
            "message": "Request body improperly formatted",
            "status": 400,
        },
        "DoesNotExist": {"message": "Invalid arguments", "status": 400},
        "AssertionError": {
            "message": "Forbidden to perform requested action",
            "status": 403,
        },
    }

    def __init__(self, error: str):
        if error in self.ERROR_MAP.keys():
            self.message = self.ERROR_MAP[error]["message"]
            self.status_code = self.ERROR_MAP[error]["status"]

        else:
            self.message = ""
            self.status_code = 400


class RequestWrapper:
    def __init__(self, request: HttpRequest, route_logic: callable, **kwargs):
        self.request = request
        self.route_logic = route_logic
        self.req_method = request.method

        if request.body:
            try:
                self.req_body = json.loads(request.body)
            except json.JSONDecodeError as e:
                raise RESTError(type(e).__name__)

        else:
            self.req_body = {}

        self.kwargs = kwargs

    def auth(self):
        cookies = self.request.COOKIES
        firebase_token = cookies.get(env("FIREBASE_COOKIE_NAME"))

        if firebase_token:
            try:
                uid = self._authenticate_user_by_token(token=firebase_token)
                user = Runner.objects.get(runner_firebase_uid=uid)

                return user
            except Exception as e:
                raise RESTError(type(e).__name__)

        else:
            raise RESTError("JSONDecodeError")

    def run(self, user: Runner):
        try:
            response = self.route_logic(
                req_body=self.req_body,
                req_method=self.req_method,
                authed_user=user,
                **self.kwargs,
            )

            return response
        except Exception as e:
            raise RESTError(type(e).__name__)

    def run_without_auth(self):
        try:
            response = self.route_logic(
                req_body=self.req_body,
                req_method=self.req_method,
                **self.kwargs,
            )

            return response
        except Exception as e:
            raise RESTError(type(e).__name__)

    def _authenticate_user_by_token(self, token: str) -> str:
        """Takes in a token and authenticates it with Firebase Auth."""
        decoded_token = auth.verify_id_token(id_token=token, check_revoked=True)
        uid = decoded_token["uid"]

        return uid


@csrf_exempt
def runs(request: HttpRequest):
    """POST: Creates a new run for authed user.
    GET: Gets list of all runs for authed user."""

    def runs_logic(
        authed_user: Runner, req_body: dict[str, str], req_method: str, **kwargs
    ):
        # GET Request
        if req_method == "GET":
            runs = Run.objects.filter(runner_id=authed_user.runner_id)

            run_list = []
            for run in runs:
                run_list.append(run.to_json())

            return JsonResponse(run_list, safe=False, status=200)

        # POST Request
        if request.method == "POST":
            date_in_seconds = int(req_body.pop("date_pub"))
            timezone_aware_date = timestamp_to_tz_date(date_in_seconds)

            new_run = Run(
                **req_body, runner_id=authed_user, date_pub=timezone_aware_date
            )  # TODO: does RESTError handle this if improperly formatted?

            new_run.save()
            new_run_json = new_run.to_json()

            return JsonResponse(new_run_json, safe=False, status=200)

        else:
            return JsonResponse(
                {
                    "message": "The HTTP Method you're calling on the api/runs/ route is not allowed."
                },
                status=405,
            )

    try:
        req_wrapper = RequestWrapper(request, runs_logic)
        authed_user = req_wrapper.auth()
        response = req_wrapper.run(authed_user)

        return response
    except RESTError as e:
        return JsonResponse({"message": e.message}, status=e.status_code)


@csrf_exempt
def run_by_id(request: HttpRequest, run_id: int):
    """GET: Get a specific run.
    DELETE: Delete a specific run"""

    def runs_by_id_logic(
        authed_user: Runner, req_body: dict[str, str], req_method: str, **kwargs
    ):
        run_id = kwargs.get("run_id")
        requested_run = Run.objects.get(run_id=run_id)
        requested_run_runner_id = requested_run.runner_id.runner_id

        assert authed_user.runner_id == requested_run_runner_id

        # GET Request
        if req_method == "GET":
            run = Run.objects.get(run_id=run_id)
            run_json = run.to_json()

            return JsonResponse(run_json, status=200, safe=False)

        # DELETE Request
        elif req_method == "DELETE":
            run = Run.objects.get(run_id=run_id)
            run.delete()

            return JsonResponse(
                {"message": f"Run with ID {run_id} succesfully deleted."},
                status=200,
            )

        else:
            return JsonResponse(
                {
                    "message": "The HTTP Method you're calling on the api/runs/:run_id route is not allowed."
                },
                status=405,
            )

    try:
        req_wrapper = RequestWrapper(request, runs_by_id_logic, run_id=run_id)
        authed_user = req_wrapper.auth()
        response = req_wrapper.run(authed_user)

        return response
    except RESTError as e:
        return JsonResponse({"message": e.message}, status=e.status_code)


@csrf_exempt
def run_map_by_id(
    request: HttpRequest, run_id: int
):  # TODO: Add in logic that calculates time and distance change and updates assocated Run's total time and total distance
    def run_map_by_id_logic(
        authed_user: Runner, req_body: dict[str, str], req_method: str, **kwargs
    ):
        run_id = kwargs.get("run_id")
        requested_run = Run.objects.get(run_id=run_id)
        requested_run_runner_id = requested_run.runner_id.runner_id

        assert authed_user.runner_id == requested_run_runner_id

        # GET Request
        if req_method == "GET":
            run_coords = RunMap.objects.filter(run_id=requested_run).values()

            run_map_json = []
            for run_map in run_coords:
                run_map_json.append(run_map)

            return JsonResponse(run_map_json, safe=False, status=200)

        # POST Request
        elif req_method == "POST":
            # Iterate over each RunMap in json data
            if isinstance(req_body, list):
                run_map_objs: list[RunMap] = []

                # convert each JSON obj to RunMap
                for map_dict in req_body:
                    map_dict["run_id"] = requested_run
                    run_map = RunMap(**map_dict)
                    run_map_objs.append(run_map)

                RunMap.objects.bulk_create(run_map_objs)  # bulk save
                requested_run.add_multiple_run_maps(
                    run_map_objs
                )  # add run maps to Run's totals

                # convert to JSON
                for i in range(len(run_map_objs)):
                    run_map_objs[i] = run_map_objs[i].to_json()

                return JsonResponse(run_map_objs, safe=False, status=200)

            else:
                req_body["run_id"] = requested_run
                map = RunMap(**req_body)
                map.save()
                requested_run.add_run_map(map)

                return JsonResponse(map.to_json(), safe=False, status=200)

        else:
            return JsonResponse(
                {
                    "message": "The HTTP Method you're calling on the api/runs/:run_id/map route is not allowed."
                },
                status=405,
            )

    try:
        req_wrapper = RequestWrapper(request, run_map_by_id_logic, run_id=run_id)
        authed_user = req_wrapper.auth()
        response = req_wrapper.run(authed_user)

        return response
    except RESTError as e:
        return JsonResponse({"message": e.message}, status=e.status_code)


@csrf_exempt
def register(
    request: HttpRequest,
):
    """POST: Calls firebase to create new user,
    creates new Runner with payload data and UID from firebase."""

    def register_logic(
        req_body: dict[str, str], req_method: str, **kwargs
    ):  # TODO: don't need authed user here, but passed to every _logic func from RESTWrapper. How can run() be more dynamic?
        if req_method == "POST":
            firebase_init = {
                "email": req_body.pop("email"),
                "password": req_body.pop("password"),
            }

            # call firebase and register user
            new_firebase_user = auth.create_user(**firebase_init)

            # create new Runner with UID
            uid = new_firebase_user.uid
            try:
                new_runner = Runner(**req_body, runner_firebase_uid=uid)
                new_runner.save()
            except Exception:
                auth.delete_user(uid)

            return JsonResponse(new_runner.to_json(), safe=False, status=200)

        else:
            return JsonResponse(
                {
                    "message": "The HTTP Method you're calling on the api/register route is not allowed."
                },
                status=405,
            )

    try:
        req_wrapper = RequestWrapper(request, register_logic)
        response = req_wrapper.run_without_auth()

        return response
    except RESTError as e:
        return JsonResponse({"message": e.message}, status=e.status_code)


@csrf_exempt
def user(request: HttpRequest):
    def user_logic(
        authed_user: Runner, req_body: dict[str, str], req_method: str, **kwargs
    ):
        assert (
            authed_user.runner_firebase_uid == req_body["runner_firebase_uid"]
        )  # TODO: rethink this name in interface?

        requested_user = Runner.objects.get(
            runner_firebase_uid=req_body["runner_firebase_uid"]
        )

        # GET Request
        if request.method == "GET":
            return JsonResponse(requested_user.to_json(), safe=False, status=200)

        # PATCH Request
        elif request.method == "PATCH":
            req_body.pop("runner_firebase_uid")

            for key in req_body.keys():
                if hasattr(requested_user, f"{key}"):
                    setattr(requested_user, f"{key}", req_body[f"{key}"])

                else:
                    raise RESTError("ValueError")

            requested_user.save()

            return JsonResponse(requested_user.to_json(), safe=False, status=200)

        else:
            return JsonResponse(
                {
                    "message": "The HTTP Method you're calling on the api/user/:user_id route is not allowed"
                },
                status=405,
            )

    try:
        req_wrapper = RequestWrapper(request, user_logic)
        authed_user = req_wrapper.auth()
        response = req_wrapper.run(authed_user)

        return response
    except RESTError as e:
        return JsonResponse({"message": e.message}, status=e.status_code)


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
