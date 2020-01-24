# Generated by Django 3.0.2 on 2020-01-24 19:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('download', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('baserequest_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='download.BaseRequest')),
                ('format', models.CharField(choices=[('bestvideo', 'Best quality video-only format'), ('bestvideo', 'Best quality audio-only format')], default='bestvideo', max_length=15, verbose_name='format')),
            ],
            options={
                'abstract': False,
            },
            bases=('download.baserequest',),
        ),
    ]
