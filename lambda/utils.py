import logging
import os
import boto3
from botocore.exceptions import ClientError

from datetime import datetime

FMT = "%H:%M"


def create_presigned_url(object_name):
    """Generate a presigned URL to share an S3 object with a capped expiration of 60 seconds

    :param object_name: string
    :return: Presigned URL as string. If error, returns None.
    """
    s3_client = boto3.client('s3',
                             region_name=os.environ.get('S3_PERSISTENCE_REGION'),
                             config=boto3.session.Config(signature_version='s3v4',s3={'addressing_style': 'path'}))
    try:
        bucket_name = os.environ.get('S3_PERSISTENCE_BUCKET')
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=60*1)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response
    


def format_time():
    starting_time = datetime.now()
    hour = (starting_time.hour + 1) % 24
    minute = starting_time.minute

    if minute < 15:
        minute  = 15
    elif minute < 30:
        minute = 30
    elif minute < 45:
        minute = 45
    else:
        minute = 0
        hour = hour + 1

    formatted_time_string = "{hour}:{minute}".format(hour = hour, minute = minute)
    current_time = datetime.strptime(formatted_time_string, FMT).time()
    formatted_time = current_time.strftime(FMT)

    return formatted_time


def calculate_diff_between_start_time_and_end_time(start_time, end_time):
    return datetime.strptime(end_time, FMT) - datetime.strptime(start_time, FMT)


def make_difference_readable(time):
    hours = int(time.seconds / 3600)
    minutes = int((time.seconds / 60) % 60)

    hours_message = ""
    if (hours == 1):
        hours_message = "one hour"
    else:
        hours_message = "{hours} hours".format(hours = hours)

    minutes_message = ""
    if (minutes > 0):
        minutes_message = " {minutes} minutes".format(minutes = minutes)

    connector_message = ""
    if (hours > 0 and minutes > 0):
        connector_message = " and "


    return "You have worked " + hours_message + connector_message + minutes_message