# Generated by Django 4.1.3 on 2023-02-03 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jokes', '0005_joke_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=50)),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='joke',
            name='tags',
            field=models.ManyToManyField(to='jokes.tag'),
        ),
    ]
