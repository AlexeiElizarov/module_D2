from django.core.management.base import BaseCommand, CommandError

from newspaper.models import Post


class Command(BaseCommand):
    help = 'Удаляет все новости/посты в указаной категории'
    missing_args_message = 'Недостаточно аргументов'

    def add_arguments(self, parser):
        parser.add_argument('arguments', nargs='+', type=str)

    def handle(self, *args, **kwargs):
        category = kwargs['arguments'][0]
        self.stdout.write(f'Do you really want to delete all posts in {category}? yes/no')
        answer = input()

        if answer == 'yes':
            Post.objects.filter(post_category__category=kwargs['arguments'][0]).delete()
            self.stdout.write(self.style.SUCCESS('Succesfully delete posts!'))
            return
        self.stdout.write(self.style.ERROR('Access denied'))
