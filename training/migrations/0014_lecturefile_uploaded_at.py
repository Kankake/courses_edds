# Generated by Django 5.1.2 on 2024-11-14 19:23

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0013_lecturefile'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturefile',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
