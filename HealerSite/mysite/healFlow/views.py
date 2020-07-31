from django.shortcuts import render
from django.http import HttpResponse
from .models import Character, RamuhTimeLine, Abilities, AbilityTimeline
from .forms import NameForm, AbilityForm
from django.http import HttpResponseRedirect
from healFlow.scripts.timeline import build_init_line, getAbilities,convert, switchTime,getGCDList, getTotalSeconds, getTotalSecondsList, getTime, createNewList
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
    ogcd_list = Abilities.objects.filter(gcd=0)
    size = AbilityTimeline.objects.filter(made=True).count()
    op_weave = build_init_line(ability_list, ramuh_list)
    if(size == 0):
        ability_list = Abilities.objects.filter(duration=30)
        op_weave = build_init_line(ability_list, ramuh_list)
        other = False
        for k, v in op_weave.items():
            abilityLine = AbilityTimeline()
            abilityLine.boss = "Ramuh"
            abilityLine.made = True
            abilityLine.ability = k
            abilityLine.times = v
            abilityLine.save()
    ability_list_line = AbilityTimeline.objects.all()
    name_time_dict = {}
    times_names = {}
    for c in ability_list_line:
        if c.ogcd == 1:
            if(c.ogcdPosition == 2):
                 name_time_dict[ "$" + c.ability] = convert(c.times)
            name_time_dict[ "@" + c.ability] = convert(c.times)
        else:
            name_time_dict[c.ability] = convert(c.times)
    print(name_time_dict)
    gcd_list = getGCDList(getTotalSeconds(ramuh_list), 1529)
    gcd_list_with_move = {}
    x = ["","",""]
    for time in gcd_list:
        times_names.update({time: x})
        gcd_list_with_move.update({time: ""})
    for name, timesList in name_time_dict.items():
        for time in timesList:
            for gcdTime in gcd_list:
                if time == gcdTime:
                    temp = []
                    if "@" in name:
                        for item in times_names[time]:
                            temp.append(item)
                        temp[1] = name
                        times_names.update({time : temp})
                    elif "$" in  name:
                        for item in times_names[time]:
                            temp.append(item)
                        temp[2] = name
                        times_names.update({time : temp})
                    else:
                        gcd_list_with_move[time] = name  
                        for item in times_names[time]:
                            temp.append(item)
                        temp[0] = name
                        times_names.update({time : temp})
    print(times_names)
    move_times = []
    move_names = []
    for c in ramuh_list:
        move_names.append(c.name)
    ramuh_times = getTotalSecondsList(ramuh_list)
    for i in range(len(ramuh_times)):
        closestTime = (min(gcd_list, key=lambda x: abs(x-ramuh_times[i])))
        move_times.append(closestTime)
        if gcd_list_with_move[closestTime] != "":
            old = gcd_list_with_move[closestTime]
            gcd_list_with_move[closestTime] = old + " / " +  move_names[i] 
        else:
            gcd_list_with_move.update({closestTime: move_names[i]})
    weave_list = Abilities.objects.filter(weave=1)
    if request.method == 'POST':
        if "time_change" in request.POST:
            swap_list = getAbilities(times_names, request.POST.get('time_change'))
            a = AbilityTimeline.objects.get(ability=swap_list[0])
            b = AbilityTimeline.objects.get(ability=swap_list[1])
            times_1, times_2 = switchTime(times_names, request.POST.get('time_change'), swap_list)
            a.times = times_1
            a.save()
        if "ogcd1_change" in request.POST:
            ocd_name = request.POST.get("ogcd1_change").split(" ")[0]
            ocd_time = request.POST.get("ogcd1_change").split(" ")[1]
            times_names = makeNewAbility(times_names, ocd_name, 1, ocd_time,1)
        elif "ogcd2_change" in request.POST:
            ocd_name = request.POST.get("ogcd2_change").split(" ")[0]
            ocd_time = request.POST.get("ogcd2_change").split(" ")[1]
            times_names = makeNewAbility(times_names, ocd_name, 1, ocd_time,2)
        else:
            makeNewAbility(times_names, request.POST.get("name"), 0, request.POST.get("time"),0)
            if request.POST.get("ogcd1") != 'None':
                makeNewAbility(times_names, request.POST.get("ogcd1"), 1, request.POST.get("time"),0)
        return HttpResponseRedirect("/timeline")
    #print(times_names)
    return render(request, 'timeline.html', {'ramuh_list': ramuh_list, 'op_weave': times_names, 
    'gcd_with_move': gcd_list_with_move, 'weave_list': weave_list, 'gcd_list': gcd_list, 
    'ogcd_list' : ogcd_list})
def makeNewAbility(times_names, name, ogcd_num, time, ogcd_change):
    if ogcd_num:
        AbilityTimeline.objects.filter(ability=name).filter(ogcdPosition=ogcd_change).delete()
    else:
        AbilityTimeline.objects.filter(ability=name).delete()
    abil_line = AbilityTimeline()   
    abil_line.boss = "Ramuh"
    abil_line.made = True
    abil_line.ogcd = ogcd_num
    abil_line.ability = name  
    abil_line.ogcdPosition = ogcd_change  
    abil_line.times = createNewList(
        times_names, name, time)
    abil_line.save()
    # if ogcd_change == 1:
    #     new_insert = "@" + name
    #     for time1, nameList in times_names.items():
    #         if time1 == int(time):
    #             for i in range(len(nameList)):
    #                 if i == ogcd_num:
    #                     print(times_names[time1][i], i)
    #                     times_names[time1][i] = "@" + name
    #                     print(times_names[time1][i], i)

    return times_names