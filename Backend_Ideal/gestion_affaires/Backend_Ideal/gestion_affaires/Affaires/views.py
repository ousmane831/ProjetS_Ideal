# views.py
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import *
from .serializers import *
from .permissions import IsAdminOrReadOnlyForExpert, IsAdministrateur, IsAdminOrReadOnly

class AnnonceViewSet(viewsets.ModelViewSet):
    queryset = Annonce.objects.all()
    serializer_class = AnnonceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'apporteuraffaires'):
            raise PermissionDenied("Seul un apporteur peut créer une annonce.")
        apporteur = self.request.user.apporteuraffaires
        serializer.save(auteur=apporteur)

    def destroy(self, request, *args, **kwargs):
        annonce = self.get_object()
        user = request.user
        
        # Seuls les administrateurs ou l'apporteur auteur peuvent supprimer
        if not (hasattr(user, 'administrateur') or 
                (hasattr(user, 'apporteuraffaires') and annonce.auteur == user.apporteuraffaires)):
            raise PermissionDenied("Vous n'avez pas la permission de supprimer cette annonce.")
        
        return super().destroy(request, *args, **kwargs)

class EvenementViewSet(viewsets.ModelViewSet):
    queryset = Evenement.objects.all()
    serializer_class = EvenementSerializer
    permission_classes = [IsAdminOrReadOnly]

class DocumentationViewSet(viewsets.ModelViewSet):
    queryset = Documentation.objects.all()
    serializer_class = DocumentationSerializer
    permission_classes = [IsAdminOrReadOnly]

class ExpertViewSet(viewsets.ModelViewSet):
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer
    permission_classes = [IsAdminOrReadOnlyForExpert]

class ApporteurAffairesViewSet(viewsets.ModelViewSet):
    queryset = ApporteurAffaires.objects.all()
    serializer_class = ApporteurAffairesSerializer
    permission_classes = [IsAdministrateur]

class ChercheurAffairesViewSet(viewsets.ModelViewSet):
    queryset = ChercheurAffaires.objects.all()
    serializer_class = ChercheurAffairesSerializer
    permission_classes = [IsAdministrateur]

class AdministrateurViewSet(viewsets.ModelViewSet):
    queryset = Administrateur.objects.all()
    serializer_class = AdministrateurSerializer
    permission_classes = [IsAdministrateur]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdministrateur]