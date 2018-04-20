import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from django.views.generic import TemplateView
from django.http import (
    FileResponse, Http404, HttpResponse, HttpResponseNotModified,
)
from django.template import Context, Engine, TemplateDoesNotExist, loader
from django.utils._os import safe_join
from django.utils.http import http_date, parse_http_date
from django.utils.translation import gettext as _, gettext_lazy

from django.shortcuts import render

from django.http import HttpResponse
	
class HomePageView(TemplateView):
    template_name = "universitytransfer/index.html"

class AboutPageView(TemplateView):
    template_name = "universitytransfer/about.html"

class NHTIPageView(TemplateView):
    template_name = "universitytransfer/nhti.html"
    
class NCCPageView(TemplateView):
    template_name = "universitytransfer/ncc.html"

class MCCPageView(TemplateView):
    template_name = "universitytransfer/mcc.html"
	
# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o): # pylint: disable=E0202
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


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
