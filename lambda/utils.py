import logging
import os
import boto3
from botocore.exceptions import ClientError

from datetime import datetime


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
    hour = starting_time.hour
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
    current_time = datetime.strptime(formatted_time_string, "%H:%M").time()
    formatted_time = current_time.strftime("%H:%M")

    return formatted_time