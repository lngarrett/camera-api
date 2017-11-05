# camera-api
IP Camera API.

## Deployment
````bash
  chalice deploy --stage main --no-autogen-policy
````

## Usage
````bash
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"camera_name":"Back Camera"}' \
  https://api.whisk.ee/camera/motion
````

## Datastore
Recent notification data is stored in DynamoDB.

## Config
Configuration data is stored in [SSM Parameter Store](https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Parameters:sort=Name).
| Key                         | Type         | Description                                                         |
|-----------------------------|--------------|---------------------------------------------------------------------|
| /camera/notification_limit  | String       | The max number of notifications allowed in the time window.         |
| /camera/notification_window | String       | The time period, in minutes, to look back for recent notifications. |
| /camera/pushover_app_key    | SecureString | Pushover app key.                                                   |
| /camera/pushover_user_key   | SecureString | Pushover user key.                                                  |
| /camera/notification_table  | String       | DynamoDB table for recent notifications                             |
