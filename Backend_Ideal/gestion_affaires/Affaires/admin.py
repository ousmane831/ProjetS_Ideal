from django.contrib import admin
from .models import (
    User,
    ApporteurAffaires,
    ChercheurAffaires,
    Expert,
    Administrateur,
    Annonce,
    Documentation,
    Evenement
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'adresse', 'telephone', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser')


@admin.register(ApporteurAffaires)
class ApporteurAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)


@admin.register(ChercheurAffaires)
class ChercheurAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)


@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialite', 'localisation', 'duree_experience')
    search_fields = ('user__username', 'specialite')
    list_filter = ('localisation',)


@admin.register(Administrateur)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)


@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'auteur', 'date_publication')
    search_fields = ('titre', 'description', 'categorie')
    list_filter = ('categorie', 'date_publication')


@admin.register(Documentation)
class DocumentationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'lien')
    search_fields = ('titre', 'categorie')


@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date', 'heure_debut', 'heure_fin', 'lieu')
    list_filter = ('date', 'categorie')
    search_fields = ('titre', 'lieu', 'categorie')
