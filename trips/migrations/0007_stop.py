# Generated by Django 5.1.6 on 2025-04-28 15:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0006_trip_is_public_trip_share_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('arrival', models.DateField(blank=True, null=True)),
                ('departure', models.DateField(blank=True, null=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stops', to='trips.trip')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
