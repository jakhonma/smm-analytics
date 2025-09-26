from rest_framework import views
from apps.analytic.query import employee_kpi_data
from apps.analytic.services import ChannelSocialAccountScoreService, KPIService
from apps.formulas.formula_cache import RedisFormulaCache
from .utils import download_kpi_report
from django.http import HttpResponse


class EmployeeKPIReportDownloadView(views.APIView):
    """
    Professional variant: Excel fayl yuklab beruvchi endpoint
    """

    permission_classes = []

    def get(self, request, *args, **kwargs):
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        data = employee_kpi_data(
            request,
            year=year,
            month=month
        )
        kpi_cache = RedisFormulaCache()
        formula_service = ChannelSocialAccountScoreService(cache=kpi_cache)
        service = KPIService(data, formula_service)
        result = service.evaluate()
        buffer = download_kpi_report(data=result)
        response = HttpResponse(
        buffer,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
        response["Content-Disposition"] = 'attachment; filename="employee_kpi_report.xlsx"'
        return response