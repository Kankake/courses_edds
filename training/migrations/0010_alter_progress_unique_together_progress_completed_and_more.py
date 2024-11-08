# Generated by Django 5.1.2 on 2024-11-08 06:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0009_quizresult'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='progress',
            unique_together={('user', 'course')},
        ),
        migrations.AddField(
            model_name='progress',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='progress',
            name='last_accessed',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='progress',
            name='progress_percentage',
            field=models.IntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name='progress',
            name='progress_percent',
        ),
    ]