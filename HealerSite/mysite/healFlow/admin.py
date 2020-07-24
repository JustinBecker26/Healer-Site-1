from django.contrib import admin
from .models import Character, RamuhTimeLine, Abilities, AbilityTimeline
# Register your models here.
admin.site.register(Character)
admin.site.register(RamuhTimeLine)
admin.site.register(Abilities)
admin.site.register(AbilityTimeline)
