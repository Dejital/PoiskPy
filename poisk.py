#!/usr/bin/env python
import random
import namer

# Generating unique object IDs

next_object_id = 1

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

class Being:
	def __init__(self):
	    self.name = ""
	    self.race = "being"
	    self.state = 'healthy'
	    self.city = None
	    self.room = None
	    self.id = 0
	    self.hp = 0
	    objects[self.id] = "Being"

	def get_name(self):
		name = ""
		if self.state == "dead":
			name += "the corpse of "
		if self.name:
			name += self.name
		else:
			name += "a %s" % self.race
		return name

	def get_short_desc(self):
		short_desc = ""
		if self.state == "dead":
			short_desc += "corpse of a "
		short_desc += self.race
		if self.name:
			short_desc += " named %s" % self.name
		return short_desc

class Player(Being):
	def __init__(self):
		Being.__init__(self)
		self.name = raw_input("What is your character's name? ")
		if not self.name:
			self.name = namer.character_name()
		self.race = "human"
		self.hp = 10
		self.target = None

class Character(Being):
	def __init__(self, id=0, race="human"):
		Being.__init__(self)
		self.name = namer.character_name()
		self.id = id
		self.race = race

class Creature(Being):
	def __init__(self, id=0, race="generic baddie"):
		Being.__init__(self)
		self.race = race
		self.id = id
		self.hp = random.randint(1,5)

class Location:
	def __init__(self):
		self.name = "generic place"
		self.size = 0
		self.id = 0
		self.description = "A generic location of size %s." % self.size
		self.rooms = {}

	def generate_rooms(self):
		for i in range(self.size):
			id = generate_id()
			objects[id] = "Room"
			self.rooms[id] = Room(id, "a hallway")
			self.rooms[id].description = "A passageway from one room to another."

	def spawn_humans(self, multiplier=2):
		num_humans = random.randint(1, self.size * multiplier)
		for i in range(num_humans):
			id = generate_id()
			room = self.rooms[random.choice(self.rooms.keys())]
			room.beings[id] = Character(id)

	def spawn_baddies(self, multiplier=3):
		num_baddies = random.randint(0, self.size * multiplier)
		for i in range(num_baddies):
			id = generate_id()
			room = self.rooms[random.choice(self.rooms.keys())]
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


# Generate world

def generate_world(num_cities=0, num_wilderness=0, num_dungeons=0):

	for i in range(num_cities):
		id = generate_id()
		objects[id] = "City"
		cities[id] = City(id, random.randint(3,6))

	for i in range(num_wilderness):
		id = generate_id()
		objects[id] = "Wilderness"
		wilds[id] = Wilderness(id, random.randint(3,6))

	for i in range(num_dungeons):
		id = generate_id()
		objects[id] = "Dungeon"
		dungeons[id] = Dungeon(id, random.randint(3,6))

generate_world(3,3,3)

# Commands

def help():
	print commands.keys()

def print_places():
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

def print_rooms():
	if p.city:
		print p.city.rooms.keys()
	else:
		print "%s is not currently in a city." % p.name

def get_location():
	if p.city and p.room: 
		print "%s stands in %s (%s) in %s." % (p.name, p.room.name, p.room.id, p.city.name)
	elif p.city:
		print "%s is currently in %s, but not in a room." % (p.name, p.city.name)
	else:
		print "%s is not currently anywhere." % p.name

def change_room(room):
	room = int(room)
	if room and p.city and room in p.city.rooms.keys():
		p.room = p.city.rooms[room]
	else:
		print "Please enter a valid room ID."

def look():
	if p.room:
		get_location()
		beings = p.room.beings.keys()
		for i in beings:
			being = p.room.beings[i]
			print "A %s is here [%s]." % (being.get_short_desc(), being.state)
	else:
		print "%s is not currently in a room." % p.name

def kill(target=""):
	if target:
		target(target)
	if p.target and p.target.state != "dead":
		print "%s slaughters %s." % (p.name, p.target.get_name())
		p.target.state = "dead"
		p.target = None
	else:
		print "Invalid target."
		p.target = None

def travel(target):
	target = target.lower()
	target_found = False
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
		p.city = city
		p.room = p.city.rooms[p.city.rooms.keys()[0]]
		print "%s arrives at %s." % (p.name, p.city.name)
	else:
		print "Invalid location. Type 'places' for valid locations."


def target(target):
	target = target.lower()
	target_found = False
	for c in p.room.beings.keys():
		being = p.room.beings[c]
		if being.name and target == being.name[:len(target)].lower():
			target_found = True
			break
		elif target == being.race[:len(target)].lower():
			target_found = True
			break
	if target_found:
		p.target = being
		print "%s now targets %s." % (p.name, p.target.get_name())
	else:
		print "Invalid target."
		p.target = None

	
def die():
	print "Game over."
	p.state = "dead"

# Game

commands = {
	'help': help,
	'places': print_places,
	'rooms': print_rooms,
	'where': get_location,
	'travel': travel,
	'go': change_room,
	'look': look,
	'kill': kill,
	'target': target,
	'die': die,
}

p = Player()
print "%s embarks on a journey." % p.name
print "Type 'help' for a list of commands."
travel(cities[random.choice(cities.keys())].name)

while(p.state != 'dead'):
  line = raw_input("> ")
  args = line.split()
  if len(args) > 0:
    commandFound = False
    for c in commands.keys():
      if args[0] == c[:len(args[0])]:
        if len(args) > 1:
          try: 
            commands[c](" ".join(args[1:]))
          except TypeError:
            print "This suggestion does not take an argument."
        else:
          try: 
            commands[c]()
          except TypeError:
            print "This suggestion needs a target."
        commandFound = True
        break
    if not commandFound:
      print "%s doesn't understand the suggestion." % p.name