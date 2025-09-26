from django.urls import path
from . import views

urlpatterns = [
    path("employee-kpi-report/", views.EmployeeKPIReportDownloadView.as_view(), name="employee-kpi-report"),   
]
