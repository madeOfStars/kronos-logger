import boto3

class AwsDynamo:
    def __init__(self):
        sts_client = boto3.client('sts')
        assumed_role_object=sts_client.assume_role(RoleArn="arn:aws:iam::074295620416:role/AlexaHostedSkillLambdaRole", RoleSessionName="AssumeRoleSession1")
        credentials=assumed_role_object['Credentials']

        # 2. Make a new DynamoDB instance with the assumed role credentials
        dynamodb = boto3.resource('dynamodb',
                      aws_access_key_id=credentials['AccessKeyId'],
                      aws_secret_access_key=credentials['SecretAccessKey'],
                      aws_session_token=credentials['SessionToken'],
                      region_name='eu-west-1')


    def insert():
        try:
            table = dynamodb.Table('logged_hours')
            
            table.put_item(
                Item={
                    "id": "AAA",
                    "attr1": "BBB"
                }
            )
        except ResourceNotExistsError:
            raise
        except Exception as e:
            raise e