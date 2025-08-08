from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AnnonceViewSet,
    EvenementViewSet,
    DocumentationViewSet,
    ExpertViewSet,
    ApporteurAffairesViewSet,
    ChercheurAffairesViewSet,
    AdministrateurViewSet,
    UserViewSet
)

router = DefaultRouter()
router.register(r'annonces', AnnonceViewSet)
router.register(r'evenements', EvenementViewSet)
router.register(r'documentations', DocumentationViewSet)
router.register(r'experts', ExpertViewSet)
router.register(r'apporteurs', ApporteurAffairesViewSet)
router.register(r'chercheurs', ChercheurAffairesViewSet)
router.register(r'administrateurs', AdministrateurViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
