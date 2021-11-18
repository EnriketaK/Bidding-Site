# Generated by Django 3.0.8 on 2020-07-20 14:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0021_auto_20200719_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='ended',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Winner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winner', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('won_item', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='auctions.Listing')),
            ],
        ),
    ]
