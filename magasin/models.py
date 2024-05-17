from django.db import models
from datetime import date
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField()
    email = models.EmailField()
    telephone = models.CharField(max_length=8)

    def __str__(self):
        return self.nom

class Categorie(models.Model):
    TYPE_CHOICES = [
        ("Al", "Alimentaire"),
        ("Mb", "Meuble"),
        ("Sn", "Sanitaire"),
        ("Vs", "Vaisselle"),
        ("Vt", "Vêtement"),
        ("Jx", "Jouets"),
        ("Lg", "Linge de Maison"),
        ("Bj", "Bijoux"),
        ("Dc", "Décor"),
    ]
    name = models.CharField(max_length=50, choices=TYPE_CHOICES, default="Alimentaire")

    def __str__(self):
        return self.name

class Produit(models.Model):
    type_choices = [("fr", "frais"), ("cs", "conserver"), ("em", "emballé")]
    libelle = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=3)
    type = models.CharField(max_length=2, choices=type_choices, default="em")
    Img = models.ImageField(blank=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.libelle} - {self.description} - {self.prix} - {self.type}"

class ProduitNC(Produit):
    duree_garantie = models.CharField(max_length=100)

    def __str__(self):
        return f"{super().__str__()} - Garantie: {self.duree_garantie}"

class Commande(models.Model):
    dateCde = models.DateField(null=True, default=date.today)
    produits = models.ManyToManyField('Produit', related_name="commandes")
    totalCde = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)

    def calculate_total(self):
        self.totalCde = sum(produit.prix for produit in self.produits.all())
        self.save()

    def __str__(self):
        product_list = ", ".join([str(p) for p in self.produits.all()])
        return f"Commande du {self.dateCde} - Total: {self.totalCde} - Produits: {product_list}"

@receiver(m2m_changed, sender=Commande.produits.through)
def update_order_total(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.calculate_total()