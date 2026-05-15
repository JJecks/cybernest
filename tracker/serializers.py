from rest_framework import serializers
from .models import Machine, AppUsageLog, BrowserVisitLog, PrintLog


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'


class AppUsageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUsageLog
        fields = '__all__'


class BrowserVisitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrowserVisitLog
        fields = '__all__'


class PrintLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintLog
        fields = '__all__'