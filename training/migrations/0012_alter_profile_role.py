# Generated by Django 5.1.2 on 2024-11-13 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0011_rename_completed_at_quizresult_date_taken_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('operator', 'Operator'), ('instructor', 'Instructor'), ('admin', 'Admin')], default='operator', max_length=20),
        ),
    ]
