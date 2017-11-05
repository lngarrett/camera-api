"""Camera API."""
import logging
import sys
from chalice import Chalice
from chalicelib import pushover, dynamodb, ssm

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
if LOGGER.handlers:
    for log_handler in LOGGER.handlers:
        LOGGER.removeHandler(log_handler)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

app = Chalice(app_name='camera-api')
app.debug = True

NOTIFICATION_WINDOW = int(ssm.get_parameter('notification_window'))
NOTIFICATION_LIMIT = int(ssm.get_parameter('notification_limit'))

@app.route('/motion', methods=['POST'])
def motion():
    """Check for recent motion. Send motion alert."""
    body = app.current_request.json_body
    camera_name = body['camera_name']
    dynamodb.put_notification(camera_name=camera_name)
    recent_notifications = dynamodb.get_recent_notifications(
        camera_name=camera_name,
        minutes=NOTIFICATION_WINDOW
    )
    notification_count = len(recent_notifications)
    if notification_count < NOTIFICATION_LIMIT:
        pushover.notification('Motion detected: {}'.format(camera_name))
        response = "{} motion. Sending push notification.".format(camera_name)
    else:
        response = (
            "{} motion. {} alerts sent within {} minutes."
            "The limit is {}. Skipping alert.").format(
                camera_name,
                notification_count,
                NOTIFICATION_WINDOW,
                NOTIFICATION_LIMIT
            )
    LOGGER.info(response)
    return {'response': response}
