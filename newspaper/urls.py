from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('search/', PostSearchView.as_view(), name='post_search'),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('<str:category>/', PostListForCategriesView.as_view(), name='category_list'),
    path('<str:category>/subscribe/', subscribe_user, name='subscribe'),

]

