from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    context={'val':"Menu Acceuil"}
    return render(request, 'acceuil.html', context)

