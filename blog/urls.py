from django.urls import path
from . import views
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('list', views.PostList.as_view(), name='post_list'),
    path('post/new/', views.PostCreate.as_view(), name='post_new'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/<int:pk>/edit/', views.PostUpdate.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDelete.as_view(), name='post_delete'),
]
