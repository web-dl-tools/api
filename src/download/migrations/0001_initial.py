# Generated by Django 3.0.2 on 2020-01-22 19:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('pre_processing', 'Pre processing'), ('downloading', 'Downloading'), ('post_processing', 'Post processing'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=15, verbose_name='status')),
                ('url', models.URLField(verbose_name='url')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]