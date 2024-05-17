from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
 


def home(request):
    posts = Post.objects.all().order_by('-created_on')  
    return render(request, 'home.html', {'posts': posts})
  
class PostList(ListView):
    model = Post
    template_name = 'post_list.html' 

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'slug', 'content', 'status', 'image']  
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user  
        return super().form_valid(form)

class PostDetail(DetailView):
    template_name = 'post_detail.html'
    model = Post

class PostUpdate(UpdateView):
    model = Post
    template_name = 'post_form.html'
    fields = "__all__"
    success_url = reverse_lazy('post_list')

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
