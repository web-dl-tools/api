# Generated by Django 3.2 on 2021-05-14 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourcerequest',
            name='delay',
            field=models.IntegerField(default=0, verbose_name='delay'),
        ),
    ]
