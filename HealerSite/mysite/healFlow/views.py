from django.shortcuts import render
from django.http import HttpResponse
from .models import Character, RamuhTimeLine, Abilities, AbilityTimeline
from .forms import NameForm, AbilityForm
from django.http import HttpResponseRedirect
from healFlow.scripts.timeline import build_init_line, convert, getGCDList, getTotalSeconds, getTotalSecondsList, getTime, createNewList
import copy


def index(request):
    return render(request, 'home.html')


def characters(request):
    character_list = Character.objects.all()
    context = {'character_list': character_list}
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            if Character.objects.filter(name=form.cleaned_data['name']).count() == 0:
                char = Character()
                char.name = form.cleaned_data['name']
                char.job = form.cleaned_data['job']
                char.weapon_damage = form.cleaned_data['weapon_damage']
                char.mind = form.cleaned_data['mind']
                char.determination = form.cleaned_data['determination']
                char.save()
    return render(request, 'characters.html', context)


def test(request):
    return render(request, 'test.html')


def timeline(request):
    ramuh_list = RamuhTimeLine.objects.all()
    ability_list = Abilities.objects.all()
    abilityLine = AbilityTimeline()
    size = AbilityTimeline.objects.filter(made=True).count()
    op_weave = build_init_line(ability_list, ramuh_list)
    if(size == 0):
        ability_list = Abilities.objects.filter(duration=30)
        op_weave = build_init_line(ability_list, ramuh_list)
        abilityLine.boss = "Ramuh"
        abilityLine.made = True
        for k, v in op_weave.items():
            abilityLine.ability = k
            abilityLine.times = v
        abilityLine.save()
    ability_list_line = AbilityTimeline.objects.all()
    times = []
    names = []
    times_names = {}
    for c in ability_list_line:
        times.append(convert(c.times))
        names.append(c.ability)
    gcd_list = getGCDList(getTotalSeconds(ramuh_list), 1529)
    gcd_list_with_move = {}
    for time in gcd_list:
        gcd_list_with_move.update({time: ""})
    zip_list = zip(names, times)
    for name, timeList in zip_list:
        for time in timeList:
            for gcdTime in gcd_list:
                if time == gcdTime:
                    gcd_list_with_move.update({time: name})
    move_times = []
    move_names = []
    times_names = copy.copy(gcd_list_with_move)

    for c in ramuh_list:
        move_names.append(c.name)
    ramuh_times = getTotalSecondsList(ramuh_list)
    for i in range(len(ramuh_times)):
        thing = (min(gcd_list, key=lambda x: abs(x-ramuh_times[i])))
        move_times.append(thing)
        if gcd_list_with_move[thing] != "":
            old = gcd_list_with_move[thing]
            gcd_list_with_move.update({thing: old + " / " + move_names[i]})
        else:
            gcd_list_with_move.update({thing: move_names[i]})
    weave_list = Abilities.objects.filter(weave=1)
    if request.method == 'POST':
        abil_line = AbilityTimeline()
        abil_line.boss = "Ramuh"
        abil_line.ability = request.POST.get("name")
        abil_line.times = createNewList(
            times_names, request.POST.get('name'), request.POST.get('time'))
        abil_line.save()
        return HttpResponseRedirect("/timeline")
    return render(request, 'timeline.html', {'ramuh_list': ramuh_list, 'op_weave': times_names, 'gcd_with_move': gcd_list_with_move, 'weave_list': weave_list})
