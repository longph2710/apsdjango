from dataclasses import fields
from rest_framework import serializers

from django_apscheduler.models import DjangoJob, DjangoJobExecution

from core.models import BackupHistory

class JobSerializer(serializers.ModelSerializer):
    class Meta():
        model = DjangoJob
        fields = '__all__'

class ExecutionSerializer(serializers.ModelSerializer):
    class Meta():
        model = DjangoJobExecution
        fields = '__all__'

class BackupSerializer(serializers.ModelSerializer):
    class Meta():
        model = BackupHistory
        fields = '__all__'