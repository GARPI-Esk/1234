from datetime import datetime, timedelta
from math import *

import matplotlib.pyplot as plt
from prettytable import *
from pyorbital.orbital import Orbital

satellites = ["NOAA 18", "NOAA 19", "METEOR-M 2", "METEOR-M2 2", "METOP-B", "METOP-C", "FENGYUN 3B", "FENGYUN 3C"]


def out_elevation(orb):
    for satPass in orb.get_next_passes(now, 60, 37.498553, 55.930383, 0.184, horizon=55):
        iop = 0
        time = satPass[2]
        print(" ", str(round(orb.get_observer_look(time, 37.498553, 55.930383, 0.184)[1], 3)))

        break


def change_satellite():
    global mnst
    global times_of_stellites
    for i in range(8):
        orb = Orbital(satellites[i], "weather.txt")
        a = orb.get_next_passes(now, 12, 37.498691, 55.930633, 0.184, horizon=55)
        # print(a)
        if len(a) == 0:
            times_of_stellites[i] = now + timedelta(weeks=6)
        else:
            times_of_stellites[i] = a[0][0]
            mnst.append(i)


def choice_satellite():
    random = 0
    for i in mnst:
        random += 1
        print(times_of_stellites[i].strftime("%d %H:%M:%S"), satellites[i], "[", random, ']', end='')
        orb = Orbital(satellites[i], "weather.txt")
        out_elevation(orb)
    print("Выберите спутник")
    a = int(input())
    return mnst[a - 1]


def time_phases_flying(f, s):
    for satPass in orb.get_next_passes(now, 60, 37.498553, 55.930383, 0.184, horizon=55):
        iop = 0
        s.write("начало,конец,зенит:\n")
        for time in satPass:
            print(time.strftime("%d:%m:%y %H:%M:%S"), end="\t\t")
            f.write(time.strftime("%d:%m:%y %H:%M:%S") + "\n")
            s.write(time.strftime("%d:%m:%y %H:%M:%S") + "\n")
            iop += 1
            if iop == 3:
                f.write(str(round(orb.get_observer_look(time, 37.498553, 55.930383, 0.184)[1], 3)) + "\n")
                s.write("высота при зените:\n" + str(
                    round(orb.get_observer_look(time, 37.498553, 55.930383, 0.184)[1], 3)) + "\n")
        print()
        break


def copters_coordinates(f, s):
    global x
    circle1 = plt.Circle((0, 0), 0.55, color='black', fill=False)
    line_x = plt.plot((0, 0), (-0.55, 0.55), 'red', linewidth=2)
    line_y = plt.plot((-0.55, 0.55), (0, 0), 'red', linewidth=2)
    x.field_names = ["time", "X", "Y"]
    for satPass in orb.get_next_passes(now, 12, 37.498691, 55.930633, 0.184, horizon=55):
        start = satPass[0]
        # получаем значения от первой до последней секунды нахождения над нашими координатами
        i = 0
        while (start - timedelta(seconds=1)) <= satPass[1]:
            alfa, beta = map(float, orb.get_observer_look(start, 37.498553, 55.930383, 0.184))
            beta = radians(beta)
            alfa = radians((alfa + 84.97) % 360)

            OF = float(0.77)  # фокусное расстояние (const)
            OK = OF / tan(beta)
            y1 = round(OK * cos(alfa) * -1, 3)
            x1 = round(OK * sin(alfa) * -1, 3)
            if i == 0:

                t = plt.scatter(x1, y1, color='blue')
                t.set_sizes(t.get_sizes() / 2)
            else:
                t = plt.scatter(x1, y1, color='green')
                t.set_sizes(t.get_sizes() / 36)
            x.add_row([start.strftime("%H:%M:%S"), x1, y1])
            f.write(start.strftime("%H:%M:%S") + " " + str(x1) + " " + str(y1) + "\n")
            start += timedelta(seconds=1)
            i += 1
        break
    t = plt.scatter(x1, y1, color='red')
    t.set_sizes(t.get_sizes() / 2)
    ax = plt.gca()
    ax.add_patch(circle1)
    plt.axis('scaled')
    print(x)
    s.write(str(x))
    ax.set_title(satellites[mn],fontsize=14)
    plt.show()
    print()


while True:
    x = PrettyTable()
    times_of_stellites = [None] * 8
    now = datetime.utcnow()
    mnst = []
    change_satellite()
    mn = choice_satellite()  # поиск минимума времени
    orb = Orbital(satellites[mn], "weather.txt")
    print(satellites[mn])
    print("-------------------------------------")
    filename = str(satellites[mn]).replace(" ", "") + "_" + str(
        times_of_stellites[mn].strftime("%d_%m_%y__%H_%M_%S").replace(" ", "")) + ".txt"
    with open("out.txt", 'w') as f, open(filename, 'w') as s:
        f.write(satellites[mn] + "\n")
        s.write(satellites[mn] + "\n")
        time_phases_flying(f, s)
        copters_coordinates(f, s)

# ориентир азимут 84.97 градусов, сайт https://www.omnicalculator.com/other/azimuth
"""Here, code praying to the GOD for protecting our open file wxHexEditor's bugs and other things.
This is really crucial step! Be adviced to not remove it, even if you don't believer.
print("Rahman ve Rahim olan Allah' in adiyla")
"""
