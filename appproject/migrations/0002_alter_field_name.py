# Generated by Django 5.1.1 on 2024-09-28 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appproject', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='name',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]
