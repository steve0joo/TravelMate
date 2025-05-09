# Generated by Django 5.1.5 on 2025-04-13 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0005_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='trip',
            name='share_token',
            field=models.CharField(blank=True, max_length=12, null=True, unique=True),
        ),
    ]
