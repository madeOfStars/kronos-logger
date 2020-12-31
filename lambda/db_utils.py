import os
import boto3

from ask_sdk_dynamodb.adapter import DynamoDbAdapter
from ask_sdk_core.exceptions import PersistenceException
from boto3.session import ResourceNotExistsError

class DbUtils:
    def __init__(self):
        self.ddb_region = os.environ.get('DYNAMODB_PERSISTENCE_REGION')
        self.ddb_table_name = os.environ.get('DYNAMODB_PERSISTENCE_TABLE_NAME')
        self.ddb_resource = boto3.resource('dynamodb', region_name=self.ddb_region)
        self._dynamodb_adapter = DynamoDbAdapter(table_name=self.ddb_table_name, create_table=False, dynamodb_resource=self.ddb_resource)

    @property
    def dynamodb_adapter(self):
        return self._dynamodb_adapter

    @dynamodb_adapter.setter
    def dynamodb_adapter(self, value):
        self._dynamodb_adapter = value

    def save_day(self, start_of_day, break_length, end_of_day, total_worked_hours):
        try:
            table = ddb_resource.Table(self.ddb_table_name)
            table.put_item(
                Item={
                    "id": "20201231",
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