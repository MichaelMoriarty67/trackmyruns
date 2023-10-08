from django.utils import timezone
from datetime import datetime
from geopy.distance import geodesic


def timestamp_to_tz_date(timestamp: int):
    date = datetime.fromtimestamp(timestamp)
    tz_aware_date = timezone.make_aware(date, timezone.get_current_timezone())

    return tz_aware_date


def change_in_time_and_kms(new_map, prev_map):
    new_coords = (new_map.latitude, new_map.longitude)
    prev_coords = (prev_map.latitude, prev_map.longitude)

    diff_kms = geodesic(new_coords, prev_coords).kilometers
    diff_time = new_map.timestamp - prev_map.timestamp

    return diff_kms, diff_time
