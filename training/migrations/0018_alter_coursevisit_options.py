# Generated by Django 5.1.2 on 2024-11-28 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0017_coursevisit_quizcompletion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coursevisit',
            options={'ordering': ['-visit_date']},
        ),
    ]