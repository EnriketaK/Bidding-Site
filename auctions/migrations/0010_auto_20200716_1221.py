# Generated by Django 3.0.8 on 2020-07-16 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20200715_1813'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='amount',
        ),
        migrations.AddField(
            model_name='bid',
            name='bid',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
