from rest_framework import generics, views, response
from apps.analytic.serializers import EmployeeKPISerializer
from apps.analytic.services import KPIService
from apps.employee.models import Employee
from apps.analytic.query import employee_kpi_data
from apps.formulas.formula_cache import RedisFormulaCache
from apps.formulas.services import ChannelSocialAccountScoreService
from django.core.cache import cache


# class EmployeeKPIView(generics.ListAPIView):
#     serializer_class = EmployeeKPISerializer

#     def get_queryset(self):
#         employee = Employee.objects.all()
#         return employee


class EmployeeKPIView(views.APIView):
    
    def get(self, request, *args, **kwargs):
        data = employee_kpi_data()
        # data = RedisKPICache().get_data()
        cache.clear()

        kpi_cache = RedisFormulaCache()

        formula_service = ChannelSocialAccountScoreService(cache=kpi_cache)

        service = KPIService(data, formula_service)
        result = service.evaluate()
        return response.Response(data=result)
