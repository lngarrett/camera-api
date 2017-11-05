"""Dynamodb."""
import logging
from time import time
import boto3
from . import ssm

LOGGER = logging.getLogger(__name__)
CLIENT = boto3.client('dynamodb')
TABLE_NAME = ssm.get_parameter('notification_table')

def put_notification(camera_name):
    """Put camera notification."""
    item = {
        'camera_name': {
            'S': camera_name
        },
        'created_at': {
            'N': str(int(time()))
        },
    }

    CLIENT.put_item(
        TableName='camera',
        Item=item
    )

def get_recent_notifications(camera_name, minutes):
    """Get all notifications for a camera within the past minutes."""
    now = time()
    start_time = now - (minutes * 60)
    response = CLIENT.query(
        TableName=TABLE_NAME,
        KeyConditionExpression='camera_name = :c and created_at > :t',
        ExpressionAttributeValues={
            ':c': {
                'S': camera_name,
            },
            ':t': {
                'N': str(start_time),
            }
        }
    )
    return response['Items']
