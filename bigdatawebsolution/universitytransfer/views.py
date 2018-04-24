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
from django.http import HttpResponse,JsonResponse
from universitytransfer.databaseUtils import LogUtil
from universitytransfer.databaseUtils import DynamoDbHelpers


class HomePageView(TemplateView):
    template_name = "universitytransfer/index.html"

class DynamicGraphPageView(TemplateView):
    template_name = "universitytransfer/dynamic_graph.html"

class AboutPageView(TemplateView):
    template_name = "universitytransfer/about.html"

class NHTIPageView(TemplateView):
    #template_name = "universitytransfer/nhti.html"
    
    def get(self, request, *args, **kwargs):
        # we will pass this context object into the
        # template so that we can access the data
        # list in the template
        departmentList = []
        
        departmentList.append({'id':"", 'name':"Please Select One", 'selected':'selected'})
        getDepartmentList(departmentList)
        context = {
            'departmentList': departmentList,
        }

        return render(request, "universitytransfer/nhti.html", context)

def getCourses(request):
    schoolId = request.GET.get('school_id', None)
    departmentId = request.GET.get('department_id', None)
    data = {
        'is_taken': str(schoolId) + ";" + str(departmentId)
    }
    return JsonResponse(data)

def getDepartmentList(departmentList):

    response = DynamoDbHelpers.FindDepartmentForSchoolDB(DynamoDbHelpers.nhtiUniversityId)

    # print("reasponse type=",type(response))
    # departmentList = []

    for department in response:
        # print("reasponse type=",type(department))
        departmentList.append({'id':department.get("department_id", None), 'name':department.get("name", None)})
    
    print(departmentList)

    return departmentList

class NCCPageView(TemplateView):
    template_name = "universitytransfer/ncc.html"

class MCCPageView(TemplateView):
    template_name = "universitytransfer/mcc.html"
	



def helloDynamo(request):
    outVal = "Movies from 1985<br/>"
    # response= DynamoDbHelpers.
    # for i in response['Items']:
    #     outVal = outVal + str(i['year']) + ":" + str(i['title'])+"<br/>"

    return HttpResponse("hello dynamo<br/>" + outVal)
