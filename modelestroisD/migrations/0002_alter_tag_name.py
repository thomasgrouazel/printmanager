# Generated by Django 4.2.6 on 2023-11-06 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelestroisD', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
