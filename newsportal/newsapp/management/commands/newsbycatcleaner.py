from django.core.management.base import BaseCommand, CommandError
from newsapp.models import Post, Category


class Command(BaseCommand):
    help = 'Подсказка вашей команды'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Delete all posts in {options["category"]} category? yes/no ')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('"Newsbycatcleaner" is cancelled'))
            return
        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(postCategory=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from category {category.name}'))
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Could not find category"))
