from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email',  'password','is_staff', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ApporteurAffairesSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ApporteurAffaires
        fields = ['id', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        return ApporteurAffaires.objects.create(user=user)

class ChercheurAffairesSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ChercheurAffaires
        fields = ['id', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        return ChercheurAffaires.objects.create(user=user)

class ExpertSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Expert
        fields = ['id', 'user', 'duree_experience', 'specialite', 'localisation', 'services_proposes']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        return Expert.objects.create(user=user, **validated_data)

class AdministrateurSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Administrateur
        fields = ['id', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        user.is_staff = True  # ← ESSENTIEL pour accéder à l'admin
        user.save()
        return Administrateur.objects.create(user=user)

# serializers.py

class PieceJointeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PieceJointe
        fields = ['id', 'fichier']

class AnnonceSerializer(serializers.ModelSerializer):
    auteur = serializers.StringRelatedField(read_only=True)
    pieces_jointes = PieceJointeSerializer(many=True, read_only=True)  # ← on ajoute ça

    class Meta:
        model = Annonce
        fields = '__all__'
        read_only_fields = ['auteur']


class DocumentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documentation
        fields = '__all__'


class PubliciteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicite
        fields = '__all__'



class EvenementSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Evenement
        
        fields = '__all__'



    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Informations de l'utilisateur
        data['username'] = self.user.username
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['email'] = self.user.email

        # Détection du rôle
        if hasattr(self.user, 'administrateur'):
            data['role'] = 'admin'
        elif hasattr(self.user, 'apporteuraffaires'):
            data['role'] = 'apporteur'
        elif hasattr(self.user, 'chercheuraffaires'):
            data['role'] = 'chercheur'
        elif hasattr(self.user, 'expert'):
            data['role'] = 'expert'
        else:
            data['role'] = 'user'

        return data
