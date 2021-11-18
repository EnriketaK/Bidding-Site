# Generated by Django 3.0.8 on 2020-07-14 11:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lisiting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('img', models.ImageField(upload_to='')),
                ('content', models.TextField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('categories', models.CharField(choices=[('Electronics', 'Electronics'), ('Fashion & Beauty', 'Fashion & Beauty'), ('Health', 'Health'), ('Beauty', 'Beauty'), ('Sports', 'Sports'), ('Home & Garden', 'Home & Garden')], max_length=25)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
