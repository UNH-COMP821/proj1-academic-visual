import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

from django.shortcuts import render

from django.http import HttpResponse

# Helper class to convert a DynamoDB item to JSON.
# class DecimalEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, decimal.Decimal):
#             if o % 1 > 0:
#                 return float(o)
#             else:
#                 return int(o)
#         return super(DecimalEncoder, self).default(o)


def index(request):

    return HttpResponse("Hi.")


def helloDynamo(request):

    ACCESS_ID="akey"
    SECRET_KEY="skey"

    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000", aws_access_key_id=ACCESS_ID, aws_secret_access_key=SECRET_KEY)
    table = dynamodb.Table('Movies')


    outVal = "Movies from 1985<br/>"
    response = table.query(
        KeyConditionExpression=Key('year').eq(1985)
        )
    for i in response['Items']:
        outVal = outVal + str(i['year']) + ":" + str(i['title'])+"<br/>"

    return HttpResponse("hello dynamo<br/>" + outVal)
