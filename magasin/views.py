from django.shortcuts import redirect, render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Fournisseur, Produit , Commande
from django.template import loader
from .forms import CommandeForm, ProduitForm, FournisseurForm
from rest_framework.views import APIView
from rest_framework.response import Response
from magasin.models import Categorie
from magasin.serializers import CategorySerializer,ProduitSerializer
from rest_framework import viewsets
from .forms import ProduitForm, FournisseurForm,UserRegistrationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def index(request):
    produit = Produit.objects.all()
    context = {"products": produit}
    return render(request, "magasin/mesProduits.html", context)

def vitrine(request):
    produit = Produit.objects.all()
    context = {"list": produit}
    return render(request, "magasin/vitrine.html", context)


def produit(request):
    if request.method == "POST":
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/magasin")  # Corrected the redirection here
    else:
        form = ProduitForm()
    
    return render(request, "magasin/majProduits.html", {"form": form})




def fournisseur(request):
    if request.method == "POST":
        form = FournisseurForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = FournisseurForm()
            messages.success(request, 'Fournisseur ajouté avec succès!')
        else:
            messages.error(request, 'Erreur lors de l’ajout du fournisseur.')
    else:
        form = FournisseurForm()
    
    # Re-fetch the fournisseurs list to ensure it includes the newly added one
    fournisseurs = Fournisseur.objects.all()
    
    return render(request, "magasin/majFournisseurs.html", {"form": form, "fournisseurs": fournisseurs})






class CategoryAPIView(APIView):
 def get(self, *args, **kwargs):
   categories = Categorie.objects.all()
   serializer = CategorySerializer(categories, many=True)
   return Response(serializer.data)

class ProduitAPIView(APIView):
 def get(self, *args, **kwargs):
   produits = Produit.objects.all()
   serializer = ProduitSerializer(produits, many=True)
   return Response(serializer.data)
 
class ProductViewset(viewsets.ReadOnlyModelViewSet):
  serializer_class = ProduitSerializer
  def get_queryset(self):
      queryset = Produit.objects.filter(active=True)
      category_id = self.request.GET.get('category_id')
      if category_id:
          queryset = queryset.filter(categorie_id=category_id)
      return queryset 
queryset = Produit.objects.filter(active=True)

def register(request):
   if request.method == 'POST' :
     form = UserCreationForm(request.POST)
     if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request,user)
        messages.success(request, f'Coucou {username}, Votre compte a été créé avec succès !')
        return redirect('home')
   else :
     form = UserCreationForm()
   return render(request,'registration/register.html',{'form' : form})

from .models import Commande  # Ensure this is imported

def manage_commande(request):
    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            cde = form.save()  # Save the new order and get the instance
            messages.success(request, 'New order created successfully.')
        else:
            messages.error(request, 'Failed to create the order.')
    else:
        form = CommandeForm()
        cde = None

    commandes = Commande.objects.all()  # Fetch all orders irrespective of the form submission
    return render(request, 'magasin/nouvelleCommande.html', {
        'form': form,
        'cde': cde,
        'commandes': commandes  # Always pass the orders list
    })




