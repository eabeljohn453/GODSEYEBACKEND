# Generated by Django 5.1.6 on 2025-02-26 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_detectionhistory_message_threatmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detected_at', models.DateTimeField(auto_now_add=True)),
                ('threat_type', models.CharField(max_length=255)),
            ],
        ),
    ]
