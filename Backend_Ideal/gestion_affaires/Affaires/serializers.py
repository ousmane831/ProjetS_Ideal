from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'adresse', 'telephone']

class ApporteurSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = ApporteurAffaires
        fields = ['id', 'user']

class ChercheurSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = ChercheurAffaires
        fields = ['id', 'user']

class ExpertSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Expert
        fields = ['id', 'user', 'duree_experience', 'specialite', 'localisation', 'services_proposes']

class AdministrateurSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Administrateur
        fields = ['id', 'user']

class AnnonceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annonce
        fields = '__all__'

class DocumentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documentation
        fields = '__all__'

class EvenementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evenement
        fields = '__all__'
