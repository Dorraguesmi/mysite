from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CategoryAPIView,ProduitAPIView, manage_commande
from rest_framework import routers
from magasin.views import ProductViewset, CategoryAPIView



router = routers.SimpleRouter()
router.register('produit', ProductViewset, basename='produit')
urlpatterns = [
    path("", views.index, name="index"),
    path("majProduits/", views.produit, name="produit"),
    path("majFournisseurs/", views.fournisseur, name="fournisseur"),
    path('vitrine/', views.vitrine, name='vitrine'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/',auth_views.LoginView.as_view(template_name='registration/login.html'), name = 'login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='registration/logout.html'), name ='logout'),
    path('api/category/', CategoryAPIView.as_view()),
    path('api/produits/', ProduitAPIView.as_view()),
    path('api/', include(router.urls)),
    path('register/',views.register, name = 'register'),
    path('nouvelleCommande/', manage_commande, name='manage_commande'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)