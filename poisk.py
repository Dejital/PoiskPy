#!/usr/bin/env python
from random import randint, choice
from math import sqrt
import namer

# Generating unique object IDs

next_object_id = 1

def main():
# Game
    w = World()
    w.populate_world()

    commands = {
            'about': about,
            'die': die,
            'equipment': get_equipment,
            'explore': explore,
            'go': change_room,
            'help': help,
            'inventory': get_inventory,
            'kill': kill,
            'l': look,
            'look': look,
            'loot': loot,
            'map': show_map,
            'places': print_places,
            'rooms': print_rooms,
            'status': status,
            'talk': talk,
            'target': target,
            'travel': travel,
            'wait': wait,
            'where': get_location,
            }

    p = Player()
    print "%s embarks on a journey." % p.name
    print "Type 'help' for a list of commands."
    travel(cities[choice(cities.keys())].name, w, p)

    while(p.state != 'dead'):
        line = raw_input("> ")
        args = line.split()
        if len(args) > 0:
            commandFound = False
            for c in commands.keys():
                if args[0].isdigit():
                    commands['target'](args[0], p)
                    commandFound = True
                    break
                elif args[0] == c[:len(args[0])]:
                    if len(args) > 1:
                        if c is 'kill':
                            try:
                                commands['target'](" ".join(args[1:]), p)
                                commands[c](p)
                            except TypeError:
                                print "This suggestion does not take an argument."
                        elif c is 'travel':
                            try:
                                commands[c](" ".join(args[1:]), w, p)
                            except TypeError:
                                print "This suggestion does not take an argument."
                        else:
                            try: 
                                commands[c](" ".join(args[1:]), p)
                            except TypeError:
                                print "This suggestion does not take an argument."
                    else:
                        if c is 'help':
                            try:
                                commands[c](p, commands)
                            except TypeError:
                                print "This suggestion needs a target."
                        elif c is 'about':
                            print "Type 'about <command>' to learn more about a specific command."
                        elif c is 'map':
                            commands[c](p, w)
                        else:
                            try:
                                commands[c](p)
                            except TypeError:
                                print "This suggestion needs a target."
                    commandFound = True
                    break
            if not commandFound:
                print "%s doesn't understand the suggestion." % p.name


def generate_id():
    global next_object_id
    id = next_object_id
    next_object_id += 1
    return id


# Dicts

objects = {}
cities = {}
dungeons = {}
wilds = {}

# Classes

## Beings

class Being:
    def __init__(self):
        self.name = ""
        self.race = "being"
        self.state = 'healthy'
        self.city = None
        self.room = None
        self.id = 0
        self.hp = 0
        self.maxhp = 0
        self.items = {}
        self.met = False
        objects[self.id] = "Being"

    def get_name(self):
        name = ""
        if self.state == "dead":
            name += "the corpse of "
        if self.name and self.met:
            name += self.name
        else:
            name += "a %s" % self.race
        return name

    def get_short_desc(self):
        short_desc = ""
        if self.state == "dead":
            short_desc += "corpse of a "
        short_desc += self.race
        if self.name and self.met:
            short_desc += " named %s" % self.name
        return short_desc

class Player(Being):
    def __init__(self):
        Being.__init__(self)
        self.name = raw_input("What is your character's name? ")
        if not self.name:
            self.name = namer.character_name()
        self.name = "\033[1m" + self.name + "\033[0;0m"
        self.race = "human"
        self.hp = 10
        self.maxhp = 10
        self.target = None
        self.age = 0.0

        wep_id = generate_id()
        self.w = Weapon(5, wep_id, 2, "Dagger") # beginner weapon
        self.items[wep_id] = self.w
    
    def equip(self, wep):
        self.items[wep.get_name()] = wep
        self.w = wep

class Character(Being):
    def __init__(self, id=0, race="human"):
        Being.__init__(self)
        self.name = namer.character_name()
        self.id = id
        self.race = race
        self.met = False

        tag_id = generate_id()
        tag_name = "Dogtag of %s" % self.name
        self.items[tag_id] = Item(tag_id, tag_name)

class Creature(Being):
    def __init__(self, id=0, race="generic baddie"):
        Being.__init__(self)
        self.race = race
        self.id = id
        self.hp = randint(1,5)

        drop_id = generate_id()
        self.items[drop_id] = Item(drop_id, "Rat meat")

## Places

class Location:
    def __init__(self):
        self.name = "generic place"
        self.size = 0
        self.id = 0
        self.description = "A generic location of size %s." % self.size
        self.rooms = {}
        self.coords = (0,0)

    def generate_rooms(self):
        for i in range(self.size):
            id = generate_id()
            objects[id] = "Room"
            self.rooms[id] = Room(id, "a hallway")
            self.rooms[id].description = "A passageway from one room to another."

    def spawn_humans(self, multiplier=2):
        num_humans = randint(1, self.size * multiplier)
        for i in range(num_humans):
            id = generate_id()
            room = self.rooms[choice(self.rooms.keys())]
            room.beings[id] = Character(id)

    def spawn_baddies(self, multiplier=3):
        num_baddies = randint(0, self.size * multiplier)
        for i in range(num_baddies):
            id = generate_id()
            room = self.rooms[choice(self.rooms.keys())]
            room.beings[id] = Creature(id, "rat")

class City(Location):
    def __init__(self, id=0, size=0):
        Location.__init__(self)
        self.size = size
        self.name = namer.city_name()
        self.id = id
        self.description = "A mundane and unambitious town of size %s." % self.size
        self.generate_rooms()
        self.spawn_humans()

class Wilderness(Location):
    def __init__(self, id=0, size=0):
        Location.__init__(self)
        self.id = id
        self.name = namer.wilderness_name()
        self.size = size
        self.generate_rooms()
        self.spawn_baddies()

class Dungeon(Location):
    def __init__(self, id=0, size=0):
        Location.__init__(self)
        self.id = id
        self.name = namer.dungeon_name()
        self.size = size
        self.generate_rooms()
        self.spawn_baddies()

class Room:
    def __init__(self, id=0, name="Abyss"):
        self.name = name
        self.description = "An empty space with no floor."
        self.exits = [0, 0, 0, 0] # N, E, S, W
        self.beings = {}
        self.items = {}
        self.id = id

class World:
    def __init__(self, width=4, height=4):
        self.name = "Mir"
        self.width = width
        self.height = height
        self.map = [ [None]*width for i in range(height) ]

    def populate_world(self):
        places = []
        num_cities = randint(1,max((self.width * self.height)/5,1))
        num_dungeons = randint(1,max((self.width * self.height)/5,1))
        num_wilds = self.width * self.height - num_cities - num_dungeons
        for i in range(num_cities):
            places.append("City")
        for i in range(num_dungeons):
            places.append("Dungeon")
        for i in range(num_wilds):
            places.append("Wilderness")
        for x in range(self.width):
            for y in range(self.height):
                choice = randint(0, len(places)-1)
                place = places[choice]
                id = generate_id()
                if place == "City":
                    objects[id] = "City"
                    cities[id] = City(id, randint(3,6))
                    self.map[y][x] = cities[id]
                    cities[id].coords = (x,y)
                elif place == "Dungeon":
                    objects[id] = "Dungeon"
                    dungeons[id] = Dungeon(id, randint(3,6))
                    self.map[y][x] = dungeons[id]
                    dungeons[id].coords = (x,y)
                else:
                    objects[id] = "Wilderness"
                    wilds[id] = Wilderness(id, randint(3,6))
                    self.map[y][x] = wilds[id]
                    wilds[id].coords = (x,y)
                del places[choice]
    
    def print_map(self,p):
        line = " |"
        line += "|".join(str(n) for n in range(self.width)) + "|"
        print line # Print x coordinates
        row = "-" + "+-" * self.width + "+"

        for r in range(self.height):
            print row
            line = str(r)
            for i in self.map[r]:
                line += "|"
                if p.city == i:
                    line += "\x1b[31m"
                if i.__class__.__name__ == "City":
                    line += "C"
                elif i.__class__.__name__ == "Dungeon":
                    line += "D"
                elif i.__class__.__name__ == "Wilderness":
                    line += "."
                else:
                    line += " "
                if p.city == i:
                    line += "\x1b[0m"
            line += "|"
            print line
        print row


## Items

class Item:
    def __init__(self, id=0, name="Thingamajig", description="Generic item.", weight=0):
        self.name = name
        self.id = id
        self.description = description
        self.weight = weight

class Weapon(Item):
    def __init__(self, offense, id=0, weight=0, name="Stick", description="Generic Weapon."):
        Item.__init__(self, id, name, description, weight)
        self.offense = offense

    def get_name(self):
        return self.name
    
    def get_stats(self):
        tup = ["Weapon", "Name: " + self.name, "Offense: " + str(self.offense), "ID: " + str(self.id), "Weight: " + str(self.weight)]
        return tup

# Commands

def about(command, p):
    if command == 'help':
        print "Command help prints the commands avaliable to the user."
    elif command == 'map':
        print "Command map prints the current world map."
    elif command == 'kill':
        print "Command kill will kill a target. Will also work if you type the target after the command kill."
        print "     > kill <NPC> (This will kill an NPC, assuming there is one in the room. It will also auto target NPC)"
        print "     > kill (This will attempt to kill a targeted NPC. Must already have target for 'kill' to work)"
    elif command == 'rooms':
        print "Command rooms will display the current rooms that the player can go to."
    elif command == 'go':
        print "Command go is how a player can travel between rooms at a location."
    elif command == 'target':
        print "Command target will target any NPC within the current location."
    elif command == 'about':
        print "Command about will give you more information about amy commands."
    elif command == 'travel':
        print "Command travel will make the player travel to a given location. It can be used two ways:"
        print "     > travel <location>"
        print "     > travel (x,y)"
    elif command == 'look':
        print "Command look or l will give you more information about what is within the current room."
    elif command == 'places':
        print "Command places will display all of the places located within the world."
    elif command == 'status':
        print "Command status will display the player's information."
    elif command == 'die':
        print "Command die will kill the player and quit the game."
    elif command == 'explore':
        print "Command explore will move the player to a random room."
    elif command == 'inventory':
        print "Command inventory will print the current items within the players pack."
    elif command == 'where':
        print "Command where will display where the player is currently located"
    elif command == 'wait':
        print "Command wait will wait for a given number of in-game hours."
    elif command == 'loot':
        print "Command loot will loot a body of a fallen foe."
    elif command == 'talk':
        print "Command talk will initiate a conversation with a targeted NPC."
    elif command == 'equipment':
        print "Command equipment will display the current equipment that player is using."
    else:
        print "Please enter a valid command to learn more about it."

def help(p, comm_dict):
    try:
        print comm_dict.keys()
    except AttributeError:
        print "This function takes no arguments."

def print_places(p):
    if cities.keys():
        list_cities = []
        for c in cities.keys():
            list_cities.append(cities[c].name)
        print "Cities:", ", ".join(list_cities)
    if wilds.keys():
        list_wilds = []
        for c in wilds.keys():
            list_wilds.append(wilds[c].name)
        print "Wilderness:", ", ".join(list_wilds)
    if dungeons.keys():
        list_dungeons = []
        for c in dungeons.keys():
            list_dungeons.append(dungeons[c].name)
        print "Dungeons:", ", ".join(list_dungeons)

def print_rooms(p):
    if p.city:
        print p.city.rooms.keys()
    else:
        print "%s is not currently in a city." % p.name

def get_location(p):
    if p.city and p.room: 
        print "%s stands in %s (%s) in %s." % (p.name, p.room.name, p.room.id, p.city.name)
    elif p.city:
        print "%s is currently in %s, but not in a room." % (p.name, p.city.name)
    else:
        print "%s is not currently anywhere." % p.name

def change_room(room, p):
    try:
        room = int(room)
        if room and p.city and room in p.city.rooms.keys():
            p.room = p.city.rooms[room]
        else:
            print "Please enter a valid room ID."
    except ValueError:
        print "Please enter a room number"

def get_equipment(p):
    print "Current Equipment for %s is:" % (p.name), p.w.get_stats()

def get_inventory(p):
    if p.items.keys():
        inventory = []
        for i in p.items.keys():
            inventory.append(p.items[i].name)
        print "Inventory:", ", ".join(inventory)
    else:
        print "%s is emptyhanded." % p.name

def look(p):
    if p.room:
        get_location(p)
        beings = p.room.beings.keys()
        counter = 1
        for i in beings:
            being = p.room.beings[i]
            line = ""
            if p.target == being: line += "\033[1m"
            line += "%s. A %s is here [%s]." % (counter, being.get_short_desc(), being.state)
            if p.target == being: line += "\033[0;0m"
            print line
            counter += 1
    else:
        print "%s is not currently in a room." % p.name

def kill(p):
    if p.target and p.target.state != "dead":
        roll = randint(1,6)
        if roll > 3:
            damage = (6.0 - roll)/6 * p.maxhp
            damage = int(round(damage))
            p.hp = max(1, p.hp - damage)
            print "%s (%s/%s) slaughters %s." % (p.name, p.hp, p.maxhp, p.target.get_name())
            p.target.state = "dead"
            p.target = None
        else:
            damage = (6.0 - roll)/6 * p.maxhp
            damage = int(round(damage))
            p.hp = max(0, p.hp - damage)
            print "%s (%s/%s) is defeated by %s." % (p.name, p.hp, p.maxhp, p.target.get_name())
            if p.hp <= 0:
                p.state = 'dead'
                print "Game over."
            p.target = None
    else:
        print "Invalid target."
        p.target = None

def talk(p):
    if p.target and p.target.__class__.__name__ == "Character":
        old_state = p.state[:]
        p.state = 'speaking'
        t = p.target
        topics = {
                'bye': None,
                'hp': '"My health is %s."' % t.hp,
                'id': '"My ID is %s."' % t.id,
                'name': '"My name is %s."' % t.name,
                'race': '"I was born %s."' % t.race,
                'state': '"I am currently %s."' % t.state,
                }
        while(p.state == 'speaking'):
            line = raw_input("> say ")
            topicFound = False
            for c in topics.keys():
                if not line:
                    topicFound = True
                    break
                elif line == 'topics' or line == 'help':
                    print topics.keys()
                    topicFound = True
                    break
                elif line == 'bye':
                    print '"Good bye."'
                    p.state = old_state
                    topicFound = True
                    break
                elif line == 'name':
                    print '"My name is %s."' % t.name
                    t.met = True
                    topicFound = True
                    break
                elif line == c:
                    print topics[c]
                    topicFound = True
                    break
            if not topicFound:
                print '"I have nothing to say about that topic."'
    else:
        print "Invalid target."


def loot(p):
    if p.target and p.target.state == "dead":
        if p.target.items.keys():
            for i in p.target.items.keys():
                item = p.target.items[i]
                p.items[item.id] = item
                del p.target.items[i]
                print "%s picks up a %s." % (p.name, item.name)
        else:
            print "There is nothing to loot."
    else:
        print "Invalid target."

def travel(target, w, p):
    target_found = False
    try:
        coords = tuple(abs(int(s)) for s in target[1:-1].split(','))
        if coords[0] < w.width and coords[1] < w.height:
            city = w.map[coords[1]][coords[0]]
            target_found = True
    except ValueError:
        target = target.lower()
        for c in cities.keys() + dungeons.keys() + wilds.keys():
            if c in cities.keys():
                city = cities[c]
            elif c in dungeons.keys():
                city = dungeons[c]
            elif c in wilds.keys():
                city = wilds[c]
            if target == city.name[:len(target)].lower():
                target_found = True
                break
    if target_found:
        if p.city:
            distance = (float(city.coords[0]) - p.city.coords[0])**2
            distance += (float(city.coords[1]) - p.city.coords[1])**2
            distance = sqrt(distance)
            p.age += distance
            distance = int(round(distance))
            line = "The journey took about "
            if distance > 1: 
                line += "%s days on horseback." % distance
                print line
            elif distance == 1: 
                line += "%s day on horseback." % distance
                print line
        p.city = city
        p.room = p.city.rooms[p.city.rooms.keys()[0]]
        print "%s arrives at %s." % (p.name, p.city.name)
    else:
        print "Invalid location. Type 'places' for valid locations."


def target(target, p):
    being = None
    if target.isdigit():
        target = int(target)
        try:
            being = p.room.beings[p.room.beings.keys()[int(target)-1]]
        except IndexError:
            print "Invalid target."
            p.target = None
        if being:
            p.target = being
            print "%s now targets %s." % (p.name, p.target.get_name())
    else:
        target = target.lower()
        target_found = False
        corpse = None
        for c in p.room.beings.keys():
            being = p.room.beings[c]
            if being.name and target == being.name[:len(target)].lower():
                if being.state == "dead": # Corpses are low priority targets
                    corpse = being
                else:
                    target_found = True
                    break
            elif target == being.race[:len(target)].lower():
                if being.state == "dead": # Corpses are low priority targets
                    corpse = being
                else:
                    target_found = True
                    break
        if target_found:
            p.target = being
            print "%s now targets %s." % (p.name, p.target.get_name())
        elif corpse:
            p.target = corpse
            print "%s now targets %s." % (p.name, p.target.get_name())
        else:
            print "Invalid target."
            p.target = None

def show_map(p, w):
    w.print_map(p)

def status(p):
    print "%s is %s days old." % (p.name, p.age)
    print "HP: %s/%s" % (p.hp, p.maxhp)

def wait(p):
    time = -1
    responded = False
    while not responded:
        print "Wait for how many hours? (Respond blank for until healed.)"
        time = raw_input(">> ")
        if time.isdigit() and time >= 0:
            responded = True
        elif time == "":
            responded = True
        else:
            print "Invalid input."
    if time == "":
        time = p.maxhp - p.hp
    hours = float(time)/24
    if time > 0:
        print "%s waited for %s hours." % (p.name, time)
    while p.hp < p.maxhp and time > 0:
        p.hp += 1
        time -= 1
    p.age += hours

def explore(p):
    if p.city:
        room = p.room
        while room.id == p.room.id:
            randroom = choice(p.city.rooms.keys())
            room = p.city.rooms[randroom]
        p.room = room
        print "%s enters %s (%s)." % (p.name, p.room.name, p.room.id)
    else:
        print "%s is not in a valid location." % p.name

def die(p):
    print "Game over."
    p.state = "dead"


if __name__ == '__main__':
    main()
