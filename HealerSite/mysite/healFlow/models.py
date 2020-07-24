from django.db import models
from django.core.validators import int_list_validator


class Character(models.Model):
    name = models.CharField(max_length=200)
    job = models.CharField(max_length=200)
    weapon_damage = models.FloatField(null=0)
    mind = models.FloatField(null=0)
    determination = models.FloatField(null=0)


class RamuhTimeLine(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    damage = models.FloatField(null=0)
    time = models.TimeField(null=0)
    time_seconds = models.FloatField(null=0)
    time_seconds_next_damage = models.FloatField(null=0, default=0)


class Abilities(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    potency = models.FloatField(null=0)
    cooldown = models.FloatField(null=0)
    gcd = models.FloatField(null=0)
    weave = models.FloatField(null=0)
    duration = models.FloatField(null=0)
    optimalWeave = models.FloatField(null=0)


class AbilityTimeline(models.Model):
    boss = models.CharField(max_length=200)
    ability = models.CharField(max_length=200)
    times = models.CharField(validators=[int_list_validator], max_length=100)
    made = models.BooleanField(default=False)
