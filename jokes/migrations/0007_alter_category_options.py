# Generated by Django 4.1.3 on 2023-02-07 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jokes', '0006_tag_joke_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('category',), 'verbose_name_plural': 'Categories'},
        ),
    ]
