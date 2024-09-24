# Generated by Django 5.1.1 on 2024-09-24 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appproject', '0010_remove_fieldselfrelationship_unique_together_field_subfield_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='fieldselfrelationship',
            name='unique_together_field_subfield',
        ),
        migrations.AddConstraint(
            model_name='fieldselfrelationship',
            constraint=models.UniqueConstraint(fields=('field', 'subfield'), name='unique_together_field_subfield'),
        ),
    ]
