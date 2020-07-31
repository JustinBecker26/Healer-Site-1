# get time
def build_init_line(abil_list, fight_timeline):
    total_seconds = getTotalSeconds(fight_timeline)
    op_weave_times = {}
    gcd = getGCDList(total_seconds, 1529)
    for abil in abil_list:
        op_weave_times.update({abil.name: getReappTimes(30, gcd)})
    return op_weave_times


def getTotalSeconds(fight_timeline):
    total_seconds = 0
    for mechanic in fight_timeline:
        x = str(mechanic.time).split(":")
        total_seconds = int(x[0]) * 60 + int(x[1])
    return total_seconds


def getTotalSecondsList(fight_timeline):
    total_seconds = []
    for mechanic in fight_timeline:
        x = str(mechanic.time).split(":")
        total_seconds.append(int(x[0]) * 60 + int(x[1]))
    return total_seconds


def getTime(time):
    total_seconds = []
    x = str(time).split(":")
    total_seconds = (int(x[0]) * 60 + int(x[1]))
    return total_seconds


def convert(string):
    ret_list = []
    string = string.replace("[", "")
    string = string.replace("]", "")
    str2 = string.split(", ")
    for c in str2:
        ret_list.append(int(c.split('.')[0]))
    return ret_list


def getGCD(SS):
    LevelModLvSub = 380
    LevelModLvDiv = 3300
    ActionDelay = 2500
    GCDm = ((1000 - (130 * (SS - LevelModLvSub) / LevelModLvDiv))
            * ActionDelay / 1000)

    GCDc = (GCDm / 100) * 100 / 1000 * (100 / 100)
    text = f"{GCDc:.2f}"
    return float(text)


def getGCDList(fightTime, SS):
    gcd = getGCD(SS)
    time = 0
    gcdList = []
    while time < fightTime:
        gcdList.append(round(time))
        time += gcd
    return gcdList


def getReappTimes(duration, gcdList):
    nextRe = duration
    reAppTimes = []
    reAppTimes.append(0)
    for i in range(len(gcdList)):
        if(nextRe < float(gcdList[i])):
            nextRe = gcdList[i-1] + duration
            reAppTimes.append(gcdList[i-1])
    return reAppTimes


def convertString(in_list):
    return str(in_list)


def createNewList(abil_line, abil, time ):
    times = []
    other_abil = "@" + abil
    for time1, abils in abil_line.items():
        if time1 == (int(time[0:4].replace("s", ''))):
            times.append(time1)
        else:    
            for a in abils:
                if a == abil or a == other_abil:
                    times.append(time1)
    times = convertString(times)
    return times


def switchTime(abil_line, time_swap, abils):
    times = time_swap.split(" ")
    time1 = int(times[0])
    time2 = int(times[1])
    times_1 = []
    times_2 = []
    if abils[0] == abils[1]:
        for time, ability in abil_line.items():
            if abils[0] == ability:
                times_1.append(time)
    times_1 = convertString(times_1)
    return times_1, times_2
        
def getAbilities(abil_line, times):
    abils = ["", ""]
    times = times.split(" ")
    time1 = int(times[0])
    time2 = int(times[1])
    for time, ability in abil_line.items():
        if time == time1:
            abils[0] = ability
        if time == time2:
            abils[1] = ability
    return abils