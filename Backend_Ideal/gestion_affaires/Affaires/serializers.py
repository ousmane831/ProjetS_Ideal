from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'adresse', 'telephone', 'password']
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
        return Administrateur.objects.create(user=user)

class AnnonceSerializer(serializers.ModelSerializer):
    auteur = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Annonce
        fields = '__all__'
        read_only_fields = ['auteur']

class DocumentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documentation
        fields = '__all__'



class EvenementSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Evenement
        
        exclude = ['image']  # ← cache le champ brut


    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
