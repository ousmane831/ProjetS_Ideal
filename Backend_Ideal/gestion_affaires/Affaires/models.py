from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# --- USER PRINCIPAL ---
class User(AbstractUser):
    
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return self.username

    def has_role(self):
        if hasattr(self, 'apporteuraffaires'):
            return "Apporteur"
        elif hasattr(self, 'chercheuraffaires'):
            return "Chercheur"
        elif hasattr(self, 'expert'):
            return "Expert"
        elif hasattr(self, 'administrateur'):
            return "Administrateur"
        return "Utilisateur"
    

    def creer_compte(self): # Fonction de création de compte
        # déjà géré par Django, mais ici placeholder
        
        self.save()


    def authentifier(self):# Fonction d'authentification
        return self.is_authenticated

    def modifier_son_compte(self, **kwargs):#cette fonction permet à l'utilisateur de modifier son compte
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()

    def demander_suppression_de_son_compte(self):
        #ici on veut supprimer le compte de l'utilisateur mais on ne le supprime pas directement car on peut le réactiver plus tard
        self.is_active = False ;# on désactive le compte
        self.save()

    def telecharger_documentation(self, doc):
        return doc.lien

    def voir_evenements(self):
        return Evenement.objects.all()

    def inscrire_evenement(self, evenement):
        evenement.participants.add(self)

    def contacter_experts(self):
        return Expert.objects.all()


# --- APPORTEUR D’AFFAIRES ---
class ApporteurAffaires(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def publier_annonce(self, titre, description, categorie, contact, fichier=None):
        return Annonce.objects.create(
            titre=titre,
            description=description,
            categorie=categorie,
            auteur=self,
            contact=contact,
            pieces_jointes=fichier
        )

    def demander_modification_annonce(self, annonce, **kwargs):
        for attr, value in kwargs.items():
            setattr(annonce, attr, value)
        annonce.save()

    def demander_suppression_annonce(self, annonce):
        annonce.delete()

    def consulter_annonces_publiees(self):
        return self.annonce_set.all()

    def __str__(self):
        return f"Apporteur: {self.user.username}"


# --- CHERCHEUR D’AFFAIRES ---
class ChercheurAffaires(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
# cette fonction nous permet de chercher des annonces
    def chercher_annonces(self, mot_cle=None, categorie=None):
        # ici on filtre selon les critères fournis
        
        qs = Annonce.objects.all()
        if mot_cle:
            qs = qs.filter(titre__icontains=mot_cle)
        if categorie:
            qs = qs.filter(categorie__iexact=categorie)
        return qs

    def consulter_annonce(self, annonce_id):
        return Annonce.objects.get(id=annonce_id)

    def contacter_apporteur(self, annonce):
        return annonce.contact

    def __str__(self):
        return f"Chercheur: {self.user.username}"


# --- EXPERT ---
class Expert(models.Model):
    
    services=[
        ('dedouanement', "Dédouanement"),
        ('transport', "Transport"),
        ('logistique', "Logistique"),
        ('conseil_juridique', "Conseil Juridique"),
        ('contrats', "Contrats"),
        ('financement', "Financement"),
        ('autre', "Autre"),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    duree_experience = models.PositiveIntegerField()
    specialite = models.CharField(max_length=100)
    localisation = models.CharField(max_length=100)
    services_proposes = models.CharField(max_length=50, choices=services, default='logistique')    
    def afficher_profil(self):
        return {
            "nom": self.user.username,
            "specialite": self.specialite,
            "experience": self.duree_experience,
            "localisation": self.localisation,
            "services": self.services_proposes,
        }

    def demander_de_creation_de_compte(self):
        self.user.is_active = False
        self.user.save()

    def authentifier(self):
        return self.user.is_authenticated

    def modifier_son_compte(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()

    def demander_suppression_decompte(self):
        self.user.is_active = False
        self.user.save()

    def fournir_conseil(self, sujet):
        return f"Expertise sur : {sujet} - Spécialité : {self.specialite}"

    def __str__(self):
        return f"Expert: {self.user.username}"


# --- ADMINISTRATEUR ---
class Administrateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def authentifier(self):
        return self.user.is_authenticated

    def valider_creation_compte_expert(self, expert):
        expert.user.is_active = True
        expert.user.save()

    def valider_suppression_compte(self, user):
        user.is_active = False
        user.save()

    def valider_modification_annonce(self, annonce, **kwargs):
        for attr, value in kwargs.items():
            setattr(annonce, attr, value)
        annonce.save()

    def supprimer_comptes(self, user):
        user.delete()

    def creer_compte_experts(self, **kwargs):
        expert_user = User.objects.create_user(**kwargs)
        Expert.objects.create(user=expert_user)
        return expert_user

    def ajouter_documentation(self, **kwargs):
        return Documentation.objects.create(**kwargs)

    def modifier_documentation(self, doc, **kwargs):
        for attr, value in kwargs.items():
            setattr(doc, attr, value)
        doc.save()

    def supprimer_documentation(self, doc):
        doc.delete()

    def ajouter_evenement(self, **kwargs):
        return Evenement.objects.create(**kwargs)

    def modifier_evenement(self, event, **kwargs):
        for attr, value in kwargs.items():
            setattr(event, attr, value)
        event.save()

    def supprimer_evenement(self, event):
        event.delete()

    def __str__(self):
        return f"Administrateur: {self.user.username}"


# --- ANNONCE ---
class Annonce(models.Model):
      
    categories=[
        ('opportunites_affaires', "Opportunités d'Affaires"),
        ('offres_services', "Offres de Services"),
        ('recherche_partenaires', "Recherche de Partenaires"),
        ('conseil_juridique', "Conseil Juridique"),
        ('autre', "Autre")
    ]
    titre = models.CharField(max_length=200)
    description = models.TextField()
    categorie = models.CharField(max_length=50, choices=categories ,default='opportunites_affaires')
    date_publication = models.DateTimeField(auto_now_add=True)
    auteur = models.ForeignKey(ApporteurAffaires, on_delete=models.CASCADE)
    contact = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)  # Si ce n’est pas toujours requis
    lieu = models.CharField(max_length=100, default='Non spécifié')

    def est_recente(self):
        return (timezone.now() - self.date_publication).days <= 7

    def __str__(self):
        return self.titre


class PieceJointe(models.Model):
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='pieces_jointes')
    fichier = models.FileField(upload_to='annonces/')
    
    def __str__(self):
        return f"Fichier {self.id} pour {self.annonce.titre}"


# --- DOCUMENTATION ---
class Documentation(models.Model):
    
    CATEGORIE_CHOICES = [
        ("commerciale", "Commerciale"),
        ("juridique", "Juridique"),
        ("technique", "Technique"),
        ("autre", "Autre"),
    ]
    titre = models.CharField(max_length=255)
    categorie = models.CharField(max_length=50, choices=CATEGORIE_CHOICES)
    contenu = models.TextField()
    lien = models.URLField(blank=True, null=True)

    def consulter_resume(self):
        return self.contenu[:150] + "..."

    def __str__(self):
        return self.titre



class Tag(models.Model):
    nom = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nom


# --- EVENEMENT ---
class Evenement(models.Model):
    
    CATEGORIE_CHOICES = [
        ('opportunites', "Opportunités d'affaires"),
        ('networking', "Networking"),
        ('formation', "Formation"),
        ('conference', "Conférence"),
        ('atelier', "Atelier"),
        # Ajoute ici d'autres catégories si besoin
    ]
   
    titre = models.CharField(max_length=200)
    description = models.TextField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    date = models.DateField()
    lieu = models.CharField(max_length=255)
    image = models.ImageField(upload_to='evenements/', null=True, blank=True)
    categorie = models.CharField(max_length=50, choices=CATEGORIE_CHOICES)
    tags = models.ManyToManyField(Tag, blank=True)
    lien_inscription = models.URLField(blank=True, null=True)
    

    def est_en_cours(self):
        now = timezone.now()
        return self.date == now.date() and self.heure_debut <= now.time() <= self.heure_fin

    def __str__(self):
        return self.titre


# --- Publicite ---
class Publicite(models.Model):
      
    titre = models.CharField(max_length=200)
    # description = models.TextField()
    contenu = models.TextField()
    badge = models.CharField(max_length=200)
    image = models.ImageField(upload_to='publicites/', null=True, blank=True)
    date_publication = models.DateTimeField(auto_now_add=True)
    contact = models.CharField(max_length=100)
    lien = models.URLField(blank=True, null=True)
    def __str__(self):
        return self.titre