from django.contrib import admin

from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'date', 'title_post', 'body_post', 'rating_post', 'on_stock')
    list_filter = ('author', 'date')
    search_fields = ('title_post', )


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'rating_author')
    list_filter = ('full_name', 'user')
    search_fields = ('user',)





admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)
