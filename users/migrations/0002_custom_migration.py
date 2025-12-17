from django.utils.text import slugify
from django.db import migrations, models
from ..models import Tags


# Create new field and populate it
def populate_tags(apps, schema_editor):
    for Tags in Tags.objects.all():
        Tags.slug = slugify(Tags.name)
        Tags.save()


def clear_slugs(apps, schema_editor):
    Tags.objects.update(slug='')
    

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            populate_tags,
            clear_slugs
        ),
    ]