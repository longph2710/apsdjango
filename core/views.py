from django.shortcuts import render
# django rest framework import
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import *

from django.contrib.auth.models import User
from django_apscheduler.models import DjangoJob, DjangoJobExecution

from .scheduler import django_scheduler as scheduler
from .models import JobExe
from .serializers import JobSerializer, ExecutionSerializer

import json
# Create your views here.

# List all job is stored in database
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAdminUser])
def list_job(request):
    jobs = DjangoJob.objects.all()
    response = JobSerializer(jobs, many=True)
    return Response(response.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAdminUser])
def list_history(request):
    data = {}
    for key in request.GET:
        data[key] = request.GET[key]
    print(data)
    executions = DjangoJobExecution.objects.filter(**data)
    # print(executions.query)
    response = ExecutionSerializer(executions, many=True)
    return Response(response.data)

# Update job with specific id with **kwargs
@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAdminUser])
def update_job(request, id):
    data = request.data

    job = scheduler.get_job(job_id=id)
    job.pause()
    job.reschedule(trigger='interval', **data)
    job.resume()

    return Response({"message" : "ok"})

# Create new backup job for database has id=id
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAdminUser])
def create_job(request):
    data = request.data
    # func_data = data.copy()
    # func_data.update({'database_id' : None})
    scheduler.add_job(
        # id=job_id,                          # job id
        trigger='interval',                 # job trigger
        **data,                             # define time for trigger
        func=JobExe.job_backup_01,          # func of job to run
        kwargs=data,                   # kwargs of func
        replace_existing=True               # replace job if job id is exsited  
    )

    return Response(data, status=status.HTTP_201_CREATED)

# Delete all job in database
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAdminUser])
def delete_all_job(request):
    scheduler.remove_all_jobs()
    return Response({"message" : "deleted"}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAdminUser])
def delete_job(request, job_id):
    scheduler.remove_job(job_id=job_id)
    return Response({"message" : "deleted"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAdminUser])
def start_scheduler(request):
    scheduler.start()
    return Response({"message" : "ok"})