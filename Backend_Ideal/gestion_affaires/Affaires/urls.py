from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnnonceViewSet, EvenementViewSet, DocumentationViewSet, ExpertViewSet

router = DefaultRouter()
router.register(r'annonces', AnnonceViewSet)
router.register(r'evenements', EvenementViewSet)
router.register(r'documentations', DocumentationViewSet)
router.register(r'experts', ExpertViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
