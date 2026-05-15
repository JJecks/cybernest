from rest_framework import generics
from .models import Machine, AppUsageLog, BrowserVisitLog, PrintLog
from .serializers import (
    MachineSerializer, AppUsageLogSerializer,
    BrowserVisitLogSerializer, PrintLogSerializer
)


class MachineListCreate(generics.ListCreateAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer


class AppUsageLogCreate(generics.CreateAPIView):
    queryset = AppUsageLog.objects.all()
    serializer_class = AppUsageLogSerializer


class AppUsageLogList(generics.ListAPIView):
    serializer_class = AppUsageLogSerializer

    def get_queryset(self):
        machine_id = self.request.query_params.get('machine_id')
        if machine_id:
            return AppUsageLog.objects.filter(machine_id=machine_id).order_by('-started_at')
        return AppUsageLog.objects.all().order_by('-started_at')


class BrowserVisitLogCreate(generics.CreateAPIView):
    queryset = BrowserVisitLog.objects.all()
    serializer_class = BrowserVisitLogSerializer


class BrowserVisitLogList(generics.ListAPIView):
    serializer_class = BrowserVisitLogSerializer

    def get_queryset(self):
        return BrowserVisitLog.objects.all().order_by('-visited_at')


class PrintLogCreate(generics.CreateAPIView):
    queryset = PrintLog.objects.all()
    serializer_class = PrintLogSerializer


class PrintLogListAll(generics.ListAPIView):
    serializer_class = PrintLogSerializer

    def get_queryset(self):
        return PrintLog.objects.all().order_by('-printed_at')


class PrintLogList(generics.ListAPIView):
    serializer_class = PrintLogSerializer

    def get_queryset(self):
        machine_id = self.kwargs.get('machine_id')
        return PrintLog.objects.filter(machine_id=machine_id).order_by('-printed_at')
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


@api_view(['POST'])
def machine_heartbeat(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id)
    machine.last_seen = timezone.now()
    machine.save()
    return Response({'status': 'ok'})


class MachineListAll(generics.ListAPIView):
    queryset = Machine.objects.all().order_by('name')
    serializer_class = MachineSerializer