from rest_framework import viewsets
from rest_framework.routers import DefaultRouter

from reports.models import Feature


class FeatureViewSet(viewsets.ModelViewSet):
    model = Feature


router = DefaultRouter()
router.register(r'', FeatureViewSet)
