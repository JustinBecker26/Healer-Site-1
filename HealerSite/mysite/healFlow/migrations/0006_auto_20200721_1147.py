# Generated by Django 3.0.8 on 2020-07-21 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healFlow', '0005_auto_20200720_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ramuhtimeline',
            name='time',
            field=models.FloatField(null=0),
        ),
    ]
