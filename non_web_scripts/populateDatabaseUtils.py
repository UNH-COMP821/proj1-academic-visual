import os, time
import boto3
from botocore.exceptions import ClientError
from django.db import connections
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

class LogUtil:
    @staticmethod
    def Write(msg):
        print(msg)

class DecimalEncoder(json.JSONEncoder):
    def default(self, o): # pylint: disable=E0202
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

class DynamoDbHelpers:
    
    ACCESS_ID="akey"
    SECRET_KEY="skey"

    @staticmethod
    def CreateTable(tableName, keySchema, attributeDefinitions):
        LogUtil.Write("Start: CreateTable")
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000", aws_access_key_id=DynamoDbHelpers.ACCESS_ID, aws_secret_access_key=DynamoDbHelpers.SECRET_KEY)

        try:
            table = dynamodb.create_table(
                TableName=tableName,
                KeySchema=keySchema,
                AttributeDefinitions=attributeDefinitions,
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
            LogUtil.Write("Table status:" + str(table.table_status))
        except ClientError as ce:
            if ce.response['Error']['Code'] == 'ResourceNotFoundException':
                LogUtil.Write ("Table " + 'TABLE_NAME' + " does not exist. Create the table first and try again.")
            else:
                LogUtil.Write("Unknown exception occurred while querying for the " + 'TABLE_NAME' + " table. Printing full error:")
                LogUtil.Write(ce.response)

        LogUtil.Write("End: CreateTable")
    
    @staticmethod
    def DeleteTable(tableName):
        LogUtil.Write("start: delete table")
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000", aws_access_key_id=DynamoDbHelpers.ACCESS_ID, aws_secret_access_key=DynamoDbHelpers.SECRET_KEY)

        table = dynamodb.Table(tableName)
        table.delete()
        LogUtil.Write("end: delete table")

    @staticmethod
    def ClearTable(tableName, pe, ean, deleteKeyName, deleteSortKeyName=None):
        LogUtil.Write("start: ClearTable")
        LogUtil.Write("attempting to clear table:"+tableName)
        
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000", aws_access_key_id=DynamoDbHelpers.ACCESS_ID, aws_secret_access_key=DynamoDbHelpers.SECRET_KEY)

        table = dynamodb.Table(tableName)

        response = table.scan(
            ProjectionExpression=pe,
            ExpressionAttributeNames= ean
            )

        print(response)
        
        for i in response['Items']:

            if deleteSortKeyName==None:
                print("attempting to delete:" + deleteKeyName +"--" + str(i[deleteKeyName]))
                table.delete_item(
                    Key={
                        str(deleteKeyName):i[deleteKeyName]
                    }
                )
            else:
                print("attempting to delete:" + deleteKeyName +"--" + str(i[deleteKeyName]) + ","+deleteSortKeyName + str(i[deleteSortKeyName]))
                table.delete_item(
                    Key={
                        str(deleteKeyName):i[deleteKeyName],
                        str(deleteSortKeyName):i[deleteSortKeyName],
                    }
                )
            
        while 'LastEvaluatedKey' in response:
            response = table.scan(
                ProjectionExpression=pe,
                ExpressionAttributeNames= ean,
                ExclusiveStartKey=response['LastEvaluatedKey']
                )
            print("attempting to delete:" + str(i[deleteKeyName]))
            table.delete_item(
                Key={
                    str(deleteKeyName):i[deleteKeyName]
                }
            )

        LogUtil.Write("end: ClearTable")


    @staticmethod
    def PrintAllTables():
        print("start: printAllTables")
        #list all tables at amazon and show structure 
        dynamodb = boto3.client('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000", aws_access_key_id=DynamoDbHelpers.ACCESS_ID, aws_secret_access_key=DynamoDbHelpers.SECRET_KEY)

        awstables = dynamodb.list_tables()

        print(awstables)

        # for item in awstables:
        #   print("Table: " + item)
        #   awstables_desc= dynamodb.describe_table(item)
        #   print("Tabledescription :" + awstables_desc)
        #   # list database items
        #   awstable = dynamodb.get_table(item)
        #   if awstable.item_count > 0:
        #           db_line = awstable.scan()
        #           for i in db_line:
        #                   print("Item : " + i)

        print("End: printAllTables")

    @staticmethod
    def InsertData(tableName,item):
        print("start: insetData")
        
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000", aws_access_key_id=DynamoDbHelpers.ACCESS_ID, aws_secret_access_key=DynamoDbHelpers.SECRET_KEY)

        table = dynamodb.Table(tableName)

        table.put_item(
            Item=item
        )

        print("End")
    
    @staticmethod
    def PrintTableData(tableName, pe, ean):
        print("Start printTableData")
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000", aws_access_key_id=DynamoDbHelpers.ACCESS_ID, aws_secret_access_key=DynamoDbHelpers.SECRET_KEY)

        table = dynamodb.Table(tableName)
        print("scanning table:" + tableName)


        response = table.scan(
            ProjectionExpression=pe,
            ExpressionAttributeNames= ean
            )

        print(response)

        
        for i in response['Items']:
            print("reasponse type=",type(i))

            
            print(json.dumps(i, cls=DecimalEncoder))

        while 'LastEvaluatedKey' in response:
            response = table.scan(
                ProjectionExpression=pe,
                ExpressionAttributeNames= ean,
                ExclusiveStartKey=response['LastEvaluatedKey']
                )


        print("End printTableData")