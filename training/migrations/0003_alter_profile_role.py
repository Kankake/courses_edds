# Generated by Django 5.1.2 on 2024-11-03 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('operator', 'Operator'), ('instructor', 'Instructor'), ('Администратор', 'Admin')], default='operator', max_length=20),
        ),
    ]
