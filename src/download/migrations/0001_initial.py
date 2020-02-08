# Generated by Django 3.0.2 on 2020-02-08 16:44

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='modified at')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('pre_processing', 'Pre processing'), ('downloading', 'Downloading'), ('post_processing', 'Post processing'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=15, verbose_name='status')),
                ('url', models.URLField(verbose_name='url')),
                ('start_processing_at', models.DateTimeField(null=True, verbose_name='start processing at')),
                ('completed_at', models.DateTimeField(null=True, verbose_name='completed at')),
                ('title', models.CharField(blank=True, max_length=200, verbose_name='title')),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(default=dict, verbose_name='data')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_download.baserequest_set+', to='contenttypes.ContentType')),
            ],
            options={
                'db_table': 'base_request',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('level', models.IntegerField(choices=[(50, 'Critical'), (50, 'Fatal'), (40, 'Error'), (30, 'Warning'), (30, 'Warn'), (20, 'Info'), (10, 'Debug'), (0, '')], default=0, verbose_name='level')),
                ('message', models.TextField(verbose_name='message')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='download.BaseRequest', verbose_name='request')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
