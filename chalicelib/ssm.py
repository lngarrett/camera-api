"""SSM parameter store."""
import logging
import boto3

LOGGER = logging.getLogger(__name__)
APP_NAME = 'camera'
CLIENT = boto3.client('ssm')

def get_parameter(name):
    """Get parameter."""
    return CLIENT.get_parameter(
        Name="/{}/{}".format(APP_NAME, name),
        WithDecryption=True
    )['Parameter']['Value']
