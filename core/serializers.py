from dataclasses import fields
from rest_framework import serializers

from django_apscheduler.models import DjangoJob, DjangoJobExecution

class JobSerializer(serializers.ModelSerializer):
    class Meta():
        model = DjangoJob
        fields = '__all__'

class ExecutionSerializer(serializers.ModelSerializer):
    class Meta():
        model = DjangoJobExecution
        fields = '__all__'