import boto3

from boto3.session import ResourceNotExistsError

from ask_sdk_dynamodb.adapter import DynamoDbAdapter

class AwsDynamo:
    def __init__(self):
        sts_client = boto3.client('sts')
        assumed_role_object=sts_client.assume_role(RoleArn="arn:aws:iam::136065421094:role/kronos_role", RoleSessionName="kronos_role")
        credentials=assumed_role_object['Credentials']

        self.dynamodb = boto3.resource('dynamodb',
                      aws_access_key_id=credentials['AccessKeyId'],
                      aws_secret_access_key=credentials['SecretAccessKey'],
                      aws_session_token=credentials['SessionToken'],
                      region_name='eu-west-1')

        self.ddb_table_name = 'logged_hours'

        self._dynamodb_adapter = DynamoDbAdapter(table_name=self.ddb_table_name, create_table=False, dynamodb_resource=self.dynamodb)

    @property
    def dynamodb_adapter(self):
        return self._dynamodb_adapter

    @dynamodb_adapter.setter
    def dynamodb_adapter(self, value):
        self._dynamodb_adapter = value

    def save_day(self, current_date, start_of_day, break_length, end_of_day, total_worked_hours):
        try:
            table = self.dynamodb.Table(self.ddb_table_name)
            
            table.put_item(
                Item={
                    "id": current_date,
                    "start_of_day": start_of_day,
                    "break_length": break_length,
                    "end_of_day": end_of_day,
                    "total_worked_hours": total_worked_hours
                })
        except ResourceNotExistsError:
            raise PersistenceException(
                "DynamoDb table {} doesn't exist. Failed to save attributes "
                "to DynamoDb table.".format(
                    self.ddb_table_name))
        except Exception as e:
            raise PersistenceException(
                "Failed to save attributes to DynamoDb table. Exception of "
                "type {} occurred: {}".format(
                    type(e).__name__, str(e)))