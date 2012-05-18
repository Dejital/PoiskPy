import random

def character_name(gender=''):
    name = ""
    if not gender:
        gender = random.choice(('m','f'))

    if gender is 'm':
        n = open("data/male.txt",'r')
    elif gender is 'f':
        n = open("data/female.txt",'r')
    else:
        print "Error: Invalid gender type."
        return name

    names = n.read()
    names = names.split("\n")
    names.pop()
    name += random.choice(names)
    n.close()

    s = open("data/surnames.txt",'r')
    names = s.read()
    names = names.split("\n")
    names.pop()
    name += ' ' + random.choice(names)
    s.close()

    return name


def city_name():

    n = open("data/cities.txt")
    names = n.read()
    names = names.split("\n")
    names.pop()
    name = random.choice(names)
    n.close()

    return name


def wilderness_name():

    name = ""
    n = open("data/colors.txt")
    colors = n.read()
    colors = colors.split("\n")
    colors.pop()
    name += random.choice(colors)
    n.close()

    name += " "

    m = open("data/wilderness.txt")
    wild = m.read()
    wild = wild.split("\n")
    wild.pop()
    name += random.choice(wild)
    m.close()

    return name

def dungeon_name():

    name = ""
    n = open("data/colors.txt")
    colors = n.read()
    colors = colors.split("\n")
    colors.pop()
    name += random.choice(colors)
    n.close()

    name += " Dungeon"

    return name