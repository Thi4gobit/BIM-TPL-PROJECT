# Generated by Django 5.1.1 on 2024-09-24 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appproject', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomField',
            new_name='FieldSet',
        ),
        migrations.RenameModel(
            old_name='GroupField',
            new_name='Group',
        ),
        migrations.RenameModel(
            old_name='CustomService',
            new_name='Obj',
        ),
    ]
