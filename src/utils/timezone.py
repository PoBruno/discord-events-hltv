import pytz
import os

def get_timezone():
    return pytz.timezone(os.getenv('TIMEZONE_TZ', 'UTC'))
