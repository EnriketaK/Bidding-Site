# Generated by Django 3.0.8 on 2020-07-16 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auto_20200716_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
