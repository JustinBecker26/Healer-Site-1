# Generated by Django 3.0.8 on 2020-07-21 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healFlow', '0006_auto_20200721_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ramuhtimeline',
            name='time',
            field=models.TimeField(null=0),
        ),
    ]
