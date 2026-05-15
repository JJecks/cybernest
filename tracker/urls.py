from django.urls import path
from . import views

urlpatterns = [
    path('machines/', views.MachineListCreate.as_view(), name='machine-list'),
    path('machines/all/', views.MachineListAll.as_view(), name='machine-list-all'),
    path('machines/<int:machine_id>/heartbeat/', views.machine_heartbeat, name='heartbeat'), 
    path('logs/app/', views.AppUsageLogCreate.as_view(), name='app-log'),
    path('logs/app/list/', views.AppUsageLogList.as_view(), name='app-log-list'),
    path('logs/browser/', views.BrowserVisitLogCreate.as_view(), name='browser-log'),
    path('logs/browser/list/', views.BrowserVisitLogList.as_view(), name='browser-log-list'),
    path('logs/print/', views.PrintLogCreate.as_view(), name='print-log'),
    path('logs/print/list/', views.PrintLogListAll.as_view(), name='print-log-list-all'),
    path('logs/print/<int:machine_id>/', views.PrintLogList.as_view(), name='print-log-list'),
]