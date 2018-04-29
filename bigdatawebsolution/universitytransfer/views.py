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
        getDepartmentList(departmentList, DynamoDbHelpers.nhtiUniversityId)
        context = {
            'departmentList': departmentList,
            'schoolId' : DynamoDbHelpers.nhtiUniversityId
        }

        return render(request, "universitytransfer/nhti.html", context)

def getCourses(request):
    schoolId = int(request.GET.get('school_id', 0))
    departmentId = int(request.GET.get('department_id', 0))

    dbResp = DynamoDbHelpers.FindCoursesForSchool(schoolId, departmentId)

    print(dbResp)

    data = {
        'course_map': json.dumps(dbResp)
    }
    return JsonResponse(data)

def getDepartmentList(departmentList, universityId):
    response = DynamoDbHelpers.FindDepartmentForSchoolDB(universityId)

    # print("reasponse type=",type(response))
    # departmentList = []

    for department in response:
        # print("reasponse type=",type(department))
        departmentList.append({'id':department.get("department_id", None), 'name':department.get("name", None)})
    
    print(departmentList)

    return departmentList

class NCCPageView(TemplateView):

    def get(self, request, *args, **kwargs):
        # we will pass this context object into the
        # template so that we can access the data
        # list in the template
        departmentList = []
        
        departmentList.append({'id':"", 'name':"Please Select One", 'selected':'selected'})
        getDepartmentList(departmentList, DynamoDbHelpers.nccUniversityId)
        context = {
            'departmentList': departmentList,
            'schoolId' : DynamoDbHelpers.nccUniversityId
        }

        return render(request, "universitytransfer/ncc.html", context)


class MCCPageView(TemplateView):
	
    def get(self, request, *args, **kwargs):
        # we will pass this context object into the
        # template so that we can access the data
        # list in the template
        departmentList = []
        
        departmentList.append({'id':"", 'name':"Please Select One", 'selected':'selected'})
        getDepartmentList(departmentList,DynamoDbHelpers.mccUniversityId)
        context = {
            'departmentList': departmentList,
            'schoolId' : DynamoDbHelpers.mccUniversityId
        }

        return render(request, "universitytransfer/mcc.html", context)


def helloDynamo(request):
    outVal = "Movies from 1985<br/>"
    # response= DynamoDbHelpers.
    # for i in response['Items']:
    #     outVal = outVal + str(i['year']) + ":" + str(i['title'])+"<br/>"

    return HttpResponse("hello dynamo<br/>" + outVal)
