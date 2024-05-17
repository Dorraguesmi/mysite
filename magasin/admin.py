from django.contrib import admin
from .models import Categorie, Produit,Fournisseur,ProduitNC,Commande

admin.site.register(Categorie)
admin.site.register(Produit)
admin.site.register(Fournisseur)
admin.site.register(ProduitNC)
admin.site.register(Commande)