# Generated by Django 3.0.8 on 2020-07-22 17:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healFlow', '0011_ramuhtimeline_time_seconds_next_damage'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbilityTimeline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boss', models.CharField(max_length=200)),
                ('ability', models.CharField(max_length=200)),
                ('times', models.CharField(max_length=100, validators=[django.core.validators.int_list_validator])),
            ],
        ),
    ]
