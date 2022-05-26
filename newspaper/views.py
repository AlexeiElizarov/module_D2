import datetime
from time import strptime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from .models import Post, Category, Author
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import *
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver


class PostsList(ListView):
    model = Post
    template_name = 'newspaper\post_list_all.html'
    context_object_name = 'posts'
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


@ receiver (m2m_changed, sender=Post.post_category.through)
def m2m_changed_dispatcher(sender, instance, action, **kwargs):
    if action == 'post_add':
        pk_set = kwargs['pk_set'].pop()
        name_category = Category.objects.get(pk=pk_set)
        users_subscribers = User.objects.filter(subscribe=pk_set)  # users подписанные на категорию
        email_users_subscribers = [u.email for u in users_subscribers]  # почта этих users
        html_content = render_to_string(
            'newspaper/email_template.html',
            {'post': instance, 'name_category': name_category})
        msg = EmailMultiAlternatives(
            subject=f'{instance.title_post}',
            body=f"Новый пост",
            from_email='Lafen55@yandex.ru',
            to=email_users_subscribers,
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


# дженерик для создания объекта.
# Надо указать только имя шаблона и класс формы который мы написали в прошлом юните.
# Остальное он сделает за вас
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'newspaper/post_create.html'
    success_url = '/news/'

    def get_number_of_post(self):
        '''возвращает колличество постов сохраненных user за текущую дату'''
        user = self.request.user
        date_now = datetime.date.today()
        posts_user = Post.objects.filter(author__user__id=user.id)
        count = 0
        for post in posts_user:
            if post.date.date() == date_now:
                count += 1
        return count

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authors'] = self.request.user.groups.filter(name='authors').exists()
        return context

    def post(self, request, *args, **kwargs):
        post = Post(
            author=Author.objects.get(pk=request.POST['author']),
            title_post=request.POST['title_post'],
            body_post=request.POST['body_post'],
        )
        if self.get_number_of_post() <3:
            post.save()
            post.post_category.add(request.POST['post_category'])
        else:
            return render(request, 'newspaper/post_more_3.html')
        return redirect('/news')



class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'newspaper/post_edit.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset,
    # чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authors'] = self.request.user.groups.filter(name='authors').exists()
        return context


# дженерик для удаления товара
class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'newspaper/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authors'] = self.request.user.groups.filter(name='authors').exists()
        return context


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

class PostListForCategriesView(ListView):
    """Вьюха вывовдит все посты с выбранной категорией"""
    model = Post
    template_name = 'newspaper/post_list_category.html'
    context_object_name = 'posts'

    # фильтрует Post по связанной таблице. Название поля таблицы берет в self.kwargs.get('category')
    def get_queryset(self):
        return Post.objects.filter(post_category__category=self.kwargs.get('category'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_queryset()
        context['name_category'] = self.kwargs.get('category')
        # user_category - все категории на которые подписан юзер
        context['user_category'] = Category.objects.filter(subscribers=self.request.user)
        context['is_not_category'] = \
            not self.request.user.subscribe.filter(category=self.kwargs.get('category')).exists()
        return context

@login_required
def subscribe_user(request, **kwargs):
    """Получает юзера, получаем категорию на странице которой находимся, и добавляем отношение"""
    user = request.user
    category = Category.objects.get(category=kwargs['category'])
    request.user.subscribe.add(category.id)
    if not request.user.groups.filter(name='authors').exists():
        # premium_group.user_set.add(user)
        print('111')
    return redirect('/')


