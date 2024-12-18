# Generated by Django 5.1.2 on 2024-11-28 12:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0020_quizattempt'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizattempt',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quizattempt',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
