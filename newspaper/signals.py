from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Post, Category


@ receiver (m2m_changed, sender=Post.post_category.through)
def m2m_changed_dispatcher(sender, instance, action, **kwargs):
    if action == 'post_add':
        pk_set = kwargs['pk_set'].pop()
        name_category = Category.objects.get(pk=pk_set)
        users_subscribers = User.objects.filter(subscribe=pk_set)  # users подписанные на категорию
        email_users_subscribers = [u.email for u in users_subscribers]  # почта этих users
        html_content = render_to_string(
            'newspaper/email_new_post.html',
            {'post': instance, 'name_category': name_category})
        msg = EmailMultiAlternatives(
            subject=f'{instance.title_post}',
            body=f"Новый пост",
            from_email='Lafen55@yandex.ru',
            to=email_users_subscribers,
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()