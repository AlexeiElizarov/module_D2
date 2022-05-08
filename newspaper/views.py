from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .models import Post, Category, Author
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import *



class PostsList(ListView):
    model = Post
    template_name = 'newspaper\post_list.html'
    context_object_name = 'posts'
    # queryset = Post.objects.order_by('-date')
    # ordering = ['rating_post']
    paginate_by = 10
    # добавляем форм класс, чтобы получать доступ к форме через метод POST
    form_class = PostForm

    def get_categories(self):
        return Category.objects.all()

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter(),
            'form': PostForm(),
        }

class PostDetail(DetailView):
    model = Post
    template_name = 'newspaper/post.html'
    context_object_name = 'post'


class Posts(View):
    def get(self, request):
        posts = Post.objects.order_by('-date')
        p = Paginator(posts, 1)
        posts = p.get_page(request.GET.get('page', 1))
        data = {
            'posts': posts
        }
        return render(request, 'newspaper/post_list.html', data)


# дженерик для получения деталей о товаре
class PostDetailView(DetailView):
    template_name = 'newspaper/post_detail.html'
    queryset = Post.objects.all()


# дженерик для создания объекта.
# Надо указать только имя шаблона и класс формы который мы написали в прошлом юните.
# Остальное он сделает за вас
class PostCreateView(CreateView):
    template_name = 'newspaper/post_create.html'
    form_class = PostForm


class PostUpdateView(LoginRequiredMixin, UpdateView):
    # login_url = ''
    # redirect_field_name = 'redirect_to'
    template_name = 'newspaper/post_edit.html'
    form_class = PostForm


    # метод get_object мы используем вместо queryset,
    # чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(DeleteView):
    template_name = 'newspaper/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class PostSearchView(ListView):
    model = Post
    template_name = 'newspaper/post_search.html'
    context_object_name = 'posts'
    form_class = PostForm

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter(),
            'form': PostForm(),
        }





