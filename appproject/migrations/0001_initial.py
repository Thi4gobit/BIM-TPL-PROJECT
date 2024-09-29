# Generated by Django 5.1.1 on 2024-09-28 23:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('template', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=255)),
                ('template', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('template', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RuleSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customfield_field', to='appproject.field')),
                ('rule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customfield_rule', to='appproject.rule')),
            ],
        ),
        migrations.CreateModel(
            name='Obj',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(blank=True, max_length=4000, null=True)),
                ('is_identifier', models.BooleanField(default=False)),
                ('is_hidden', models.BooleanField(default=False)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customfieldvalue_item', to='appproject.item')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customfieldvalue_field', to='appproject.ruleset')),
            ],
        ),
        migrations.CreateModel(
            name='FieldLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.PositiveIntegerField()),
                ('text_before', models.CharField(blank=True, max_length=32, null=True)),
                ('text_after', models.CharField(blank=True, max_length=32, null=True)),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fieldlink_fields', to='appproject.field')),
                ('subfield', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fieldlink_subfields', to='appproject.field')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('field', 'subfield'), name='unique_together_field_subfield')],
            },
        ),
        migrations.AddConstraint(
            model_name='ruleset',
            constraint=models.UniqueConstraint(fields=('rule', 'field'), name='unique_together_rule_field'),
        ),
        migrations.AddConstraint(
            model_name='obj',
            constraint=models.UniqueConstraint(fields=('item', 'field'), name='unique_together_item_field'),
        ),
    ]
