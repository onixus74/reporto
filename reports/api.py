from rest_framework import viewsets
from rest_framework.routers import DefaultRouter

from reports.models import Report


class ReportViewSet(viewsets.ModelViewSet):
    model = Report


router = DefaultRouter()
router.register(r'', ReportViewSet)
