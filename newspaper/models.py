from django.core.cache import cache
from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    full_name = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.full_name}'

    def update_rating(self):
        count = 0
        count_posts = 0
        for post in Post.objects.filter(author__full_name=self.full_name):
            count_posts += post.rating_post
            count += count_posts * 3
        for comment in Comment.objects.filter(post__author=self):
            count += comment.rating_comment
        for comment in Comment.objects.filter(user=self.user):
            count += comment.rating_comment
        self.rating_author = count

    @staticmethod
    def get_best_author():
        best = Author.objects.all().order_by('-rating_author')[0]
        return best.user.username, best.rating_author

    def get_rating(self):
        return f'{self.rating_author}'


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, related_name='subscribe')

    def __str__(self):
        return f'{self.category}'


class Post(models.Model):
    news = 'NW'
    article = 'AR'

    POSITION = [
        (news, 'Новость'),
        (article, 'Статья')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    title_post = models.CharField(max_length=255)
    body_post = models.TextField()
    rating_post = models.IntegerField(default=1)
    position = models.CharField(max_length=2, choices=POSITION, default=news)
    post_category = models.ManyToManyField(Category, through='PostCategory')

    def __str__(self):
        return f'{self.title_post}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    @property
    def on_stock(self):
        return self.rating_post > 1

    def like(self):
        self.rating_post += 1

    def dislike(self):
        self.rating_post -= 1

    def preview(self):
        return self.body_post[:124] + '...'

    @staticmethod
    def get_best_post():
        best_post = Post.objects.all().order_by('-rating_post')[0]
        return best_post.date, best_post.author.user, best_post.rating_post, best_post.title_post, best_post.preview()

    @staticmethod
    def get_all_comment_for_best_post():
        best_post = Post.objects.all().order_by('-rating_post')[0]
        return Comment.objects.filter(post=best_post)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')




class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body_comment = models.TextField()
    date_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.body_comment[:50]}'

    def like(self):
        self.rating_comment += 1

    def dislike(self):
        self.rating_comment -= 1






