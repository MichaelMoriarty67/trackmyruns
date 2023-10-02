from django.utils import timezone
from datetime import datetime


def timestamp_to_tz_date(timestamp: int):
    date = datetime.fromtimestamp(timestamp)
    tz_aware_date = timezone.make_aware(date, timezone.get_current_timezone())

    return tz_aware_date
