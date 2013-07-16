from rest_framework import viewsets
from rest_framework.routers import DefaultRouter

from reports.models import Victim


class VictimViewSet(viewsets.ModelViewSet):
    model = Victim


router = DefaultRouter()
router.register(r'', VictimViewSet)
