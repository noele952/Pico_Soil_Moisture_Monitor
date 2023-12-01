import os
import boto3
from datetime import datetime, timedelta

SENDER_EMAIL = os.environ['SENDER_EMAIL']
RECIPIENT_EMAIL = os.environ['RECIPIENT_EMAIL']
DYNAMODB_TABLE = 'soil_moisture_notification'
REMINDER_INTERVAL_HOURS = 6

ses = boto3.client('ses')
dynamodb = boto3.client('dynamodb')

def is_first_run():
    return os.environ.get('FIRST_RUN', 'false').lower() == 'true'

def set_first_run():
    os.environ['FIRST_RUN'] = 'false'

def create_dynamodb_table(table_name):
    try:
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'email', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'email', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f'Table {table_name} created successfully.')
        set_first_run()  # Set the flag to indicate that the table has been created
    except dynamodb.exceptions.ResourceInUseException:
        print(f'Table {table_name} already exists.')
    except Exception as e:
        print(f'Error creating or checking table {table_name}: {e}')

def lambda_handler(event, context):
    if is_first_run():
        create_dynamodb_table(DYNAMODB_TABLE)

    soil_moisture = event.get('data', 'N/A')
    sensor_name  = event.get('label', 'N/A')

    # Check if there's an existing timestamp in the database
    last_reminder_time = get_last_reminder_time(RECIPIENT_EMAIL)

    # If no timestamp exists or it's been more than the defined interval
    if not last_reminder_time or is_older_than_interval(last_reminder_time):
        send_reminder_email(RECIPIENT_EMAIL, soil_moisture, sensor_name)
        save_last_reminder_time(RECIPIENT_EMAIL)

def get_last_reminder_time(email):
    try:
        response = dynamodb.get_item(
            TableName=DYNAMODB_TABLE,
            Key={'email': {'S': email}}
        )
        return response.get('Item', {}).get('timestamp', {}).get('S')
    except Exception as e:
        print(f'Error getting last reminder time: {e}')
        return None

def save_last_reminder_time(email):
    current_timestamp = str(datetime.now())
    try:
        dynamodb.put_item(
            TableName=DYNAMODB_TABLE,
            Item={'email': {'S': email}, 'timestamp': {'S': current_timestamp}}
        )
    except Exception as e:
        print(f'Error saving last reminder time: {e}')

def is_older_than_interval(timestamp):
    interval_ago = datetime.now() - timedelta(hours=REMINDER_INTERVAL_HOURS)
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f") < interval_ago

def send_reminder_email(email, soil_moisture, sensor_name):
    params = {
        'Destination': {
            'ToAddresses': [email],
        },
        'Message': {
            'Body': {
                'Text': {'Data': f'Your plant is getting dry. The moisture level is {soil_moisture}.\nPlease water it.'},
            },
            'Subject': {'Data': f'Water your plant - {sensor_name}'},
        },
        'Source': SENDER_EMAIL,
    }

    try:
        response = ses.send_email(**params)
        print(f'Email sent to {email} successfully.')
    except Exception as e:
        print(f'Error sending email to {email}: {e}')



