"""Pushover."""
import logging
import http.client
import urllib
from . import ssm

LOGGER = logging.getLogger(__name__)

TOKEN = ssm.get_parameter('pushover_app_key')
USER = ssm.get_parameter('pushover_user_key')

def notification(message):
    """Send notification."""
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request(
        "POST",
        "/1/messages.json",
        urllib.parse.urlencode({
            "token": TOKEN,
            "user": USER,
            "message": message,
        }),
        {"Content-type": "application/x-www-form-urlencoded"})
    conn.getresponse()
