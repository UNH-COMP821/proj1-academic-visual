import os, time
import boto3
from botocore.exceptions import ClientError


ACCESS_ID="akey"
SECRET_KEY="skey"

def createTables():
    
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000", aws_access_key_id=ACCESS_ID, aws_secret_access_key=SECRET_KEY)

    try:
        table = dynamodb.create_table(
            TableName='Movies',
            KeySchema=[
                {
                    'AttributeName': 'year',
                    'KeyType': 'HASH'  #Partition key
                },
                {
                    'AttributeName': 'title',
                    'KeyType': 'RANGE'  #Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'year',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'title',
                    'AttributeType': 'S'
                },

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        print("Table status:", table.table_status)
    except ClientError as ce:
        if ce.response['Error']['Code'] == 'ResourceNotFoundException':
            print ("Table " + 'TABLE_NAME' + " does not exist. Create the table first and try again.")
        else:
            print("Unknown exception occurred while querying for the " + 'TABLE_NAME' + " table. Printing full error:")
            print(ce.response)

    print("End","")



createTables()