from rest_framework import viewsets
from rest_framework.routers import DefaultRouter

from reports.models import Category


class CategoryViewSet(viewsets.ModelViewSet):
    model = Category


router = DefaultRouter()
router.register(r'', CategoryViewSet)
