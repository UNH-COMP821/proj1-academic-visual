import os, time
import boto3
from botocore.exceptions import ClientError
from django.db import connections
import json
import decimal


ACCESS_ID="akey"
SECRET_KEY="skey"

class DecimalEncoder(json.JSONEncoder):
    def default(self, o): # pylint: disable=E0202
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


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


def printAllTables():
    print("start: printAllTables")
    #list all tables at amazon and show structure 
    dynamodb = boto3.client('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000", aws_access_key_id=ACCESS_ID, aws_secret_access_key=SECRET_KEY)

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

def insetData():
    print("start: insetData")
    
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000", aws_access_key_id=ACCESS_ID, aws_secret_access_key=SECRET_KEY)

    table = dynamodb.Table('Movies')

    table.put_item(
        Item={
            'year':1985,
            'title':"1234",
            'infox':{
                'pee':"pe"
            }
        }
    )
    table.put_item(
        Item={
            'year':1986,
            'title':"321",
        }
    )

    print("End")

def printTableData():
    print("Start printTableData")
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000", aws_access_key_id=ACCESS_ID, aws_secret_access_key=SECRET_KEY)

    table = dynamodb.Table('Movies')

    print("Movies from 1985")

    #print(table.scan())

    pe ="#yr, title, infox.pee"
    # Expression Attribute Names for Projection Expression only.
    ean = { "#yr": "year", }

    response = table.scan(
        ProjectionExpression=pe,
        ExpressionAttributeNames= ean
        )

    print(response)

    
    for i in response['Items']:
        print("reasponse type=",type(i))

        # print all items in the dictionary
        # for key, value in i.items() :
        #     print(key, value)

        
        print(json.dumps(i, cls=DecimalEncoder))

        # if('infox' in i):
        #     print(i['year'], ":", i['title'], i['infox'])
        # else:
        #     print(i['year'], ":", i['title'])


    while 'LastEvaluatedKey' in response:
        response = table.scan(
            ProjectionExpression=pe,
            ExpressionAttributeNames= ean,
            ExclusiveStartKey=response['LastEvaluatedKey']
            )

        # for i in response['Items']:
        #     print("inner:" + i['year'], ":", i['title'], i['infox.pee'])

    print("End printTableData")


def deleteTable():
    print("start: delete table")
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000", aws_access_key_id=ACCESS_ID, aws_secret_access_key=SECRET_KEY)

    table = dynamodb.Table('Movies')
    table.delete()
    print("end: delete table")

#deleteTable()
#createTables()
#printAllTables()
insetData()
printTableData()
