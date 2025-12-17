from django.core.management.base import BaseCommand
from users.models import Post
from django.utils import timezone


class Command(BaseCommand):
    help = 'Delete posts older than one week'

    def handle(self, *args, **kwargs):
        one_week_ago = timezone.now() - timezone.timedelta(weeks=1)
        Post.objects.filter(created_at__lt=one_week_ago).delete()

        self.stdout.write(
            self.style.SUCCESS('Successfully deleted posts older than one week')
        )
        
