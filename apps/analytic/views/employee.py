from rest_framework import views, response, status
from apps.analytic.services import KPIService
from apps.analytic.query import employee_kpi_data
from apps.formulas.formula_cache import RedisFormulaCache
from apps.formulas.services import ChannelSocialAccountScoreService


class EmployeeKPIView(views.APIView):
    
    def get(self, request, *args, **kwargs):
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        if year is not None:
            try:
                year = int(year)
            except ValueError:
                return response.Response({"error": "Year must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
        if month is not None:
            try:
                month = int(month)
                if month < 1 or month > 12:
                    raise ValueError
            except ValueError:
                return response.Response({"error": "Month must be an integer between 1 and 12."}, status=status.HTTP_400_BAD_REQUEST)
        
        data = employee_kpi_data(
            request,
            year=year,
            month=month
        )
        kpi_cache = RedisFormulaCache()
        formula_service = ChannelSocialAccountScoreService(cache=kpi_cache)
        service = KPIService(data, formula_service)
        result = service.evaluate()
        return response.Response(data=result, status=status.HTTP_200_OK)
