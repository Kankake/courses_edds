# Generated by Django 5.1.2 on 2024-11-03 19:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0007_remove_question_correct_answer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='quiz',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_course', to='training.quiz'),
        ),
    ]
