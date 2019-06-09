import sys
import time
from data_handler import database
import threading
from map.classes import char
db = database()
promises = []
mods = ['108791316110923750592', '113117618922729693853']
'''
class promise:
	def __init__(self, command, sender, cid):
		self.cmd = command
		self.snd = sender
		self.cid = cid
		t = threading.Timer(20.0, self.delete)
		t.start()
	def delete(self):
		#should have unique cmd and snd
		send(self.cid, 'deleted')
		for i in range(0, len(promises)):
			if (promises[i].snd == self.snd and promises[i].cmd == self.cmd and promises[i].cid == self.cid):
				promises.pop(i)
				return
'''


class handler:
	def join(self, psmg, sender, cid): 
		#create new char TODO: add confirmation
		if (len(psmg) == 1):
			send(cid, 'fuck you , please specify name and world')
		elif (len(psmg) == 2):
			send(cid, 'fuck you, please specify world')
		else:
			if (db.isWorld(psmg[2])):
				import copy
				character = char(psmg[2], psmg[1])
				
				spawnpoint = db.spawn_player(character.world)
				character.pos = spawnpoint

				character.biomeID = db.getIDofPos(character.pos, character.world)

				db.setPlayer(sender, copy.deepcopy(character), 0)
				db.setPlayer(sender, [spawnpoint], 1) #char info, unmasked coordinates
				send(cid, 'Your character ' + psmg[1] + ' has been created!')
				send(cid, 'Your character has spawned at ' + str(spawnpoint) + '.')
				from map.classes import world
				world_object = db.getWorldData(psmg[2])
				world_object.players.append(sender)
				db.setWorld(-1, -1, world_object, psmg[2])
			else:
				send(cid, 'fuck you, ' + str(psmg[2]) +' isnt an existing world')
	def worldlist(self, psmg, sender, cid):
		send(cid, db.worldList())
		return
	def fullmap(self, psmg, sender, cid):
		playerExists(sender, cid)
		if (sender in mods):
			sendImage(cid, 'world map', db.getMapDir(db.getPlayerWorld(sender)))
		else:
			send(cid, 'You do not have permission to execute this command.')
		return
	def map(self, psmg, sender, cid):
		playerExists(sender, cid)
		#displays all areas player has visited
		from draw_map import draw_map
		player = db.getPlayer(sender, 0)
		pcoords = db.getPlayer(sender, 1)
		draw_map(sender, pcoords, player.world)
		sendImage(cid, 'All explored coordinates for player ' + str(player.name) + '.', 'data/players/' + str(sender) + '.png')
	def newworld(self, psmg, sender, cid):
		if (sender == '108791316110923750592' or sender == '109696714510497833957'):
			if (len(psmg) > 1):
				send(cid, 'Generating world...')
				from map.mapgen import gen_map
				gen_map(psmg[1])
			else:
				send(cid, 'Please provide a name.')
				return
		else:
			send(cid, 'You do not have permission to execute this command.')
	def inv(self, psmg, sender, cid):
		playerExists(sender, cid)
		player = db.getPlayer(sender, 0)
		sendRaw(cid, player.inventory.make_array())
	def inventory(self, psmg, sender, cid):
		self.inv(psmg, sender, cid)
	def travel(self, psmg, sender, cid):
		playerExists(sender, cid)
		import numpy as np
		import math
		player = db.getPlayer(sender, 0)
		pcoords = db.getPlayer(sender, 1)
		from misc import find_endpoint, find_uncovered
		f_c = find_endpoint(psmg[1], float(psmg[2]), player.pos)
		if (f_c == -1):
			send(cid, 'That coordinate is out of bounds!')
			return
		pythag = lambda start, end: int(math.sqrt((start[0] - end[0])**2 + (start[1] - end[1])**2))
		dist = pythag(player.pos, f_c) * 3
		if (player.hunger <= dist): #implement auto-eat later
			send(cid, "You don't have enough nutrition to survive that journey.")
			return
		player.hunger -= dist
		newcoords = find_uncovered(player.pos, f_c)

		player.pos = f_c
		player.biomeID = db.getIDofPos(player.pos, player.world)

		send(cid, str(player.name) + ' travelled to ' + str(f_c))
		send(cid, str(player.name) + "'s nutrition level is now " + str(player.hunger))

		db.setPlayer(sender, np.concatenate((pcoords, newcoords)), 1)
		db.setPlayer(sender, player, 0)
	def gather(self, psmg, sender, cid):
		playerExists(sender, cid)
		from map.classes import biome
		import configparser
		from resources import generateResources, calculateLoot
		player = db.getPlayer(sender, 0)
		p_biome = db.getBiomeByID(player.biomeID, player.world)
		if (int(psmg[1]) > 1440):
			send(cid, 'You can only gather resources for up to 1 day (1440 minutes).')
			return
		if (type(p_biome.resources) == type(-1)):
			p_biome = generateResources(p_biome)
		time_taken, player.inventory, p_biome = calculateLoot(p_biome, psmg[1], 'damascus blade', player.inventory)
		db.updateBiomeByID(player.biomeID, player.world, p_biome)
		if (time_taken != -1):
			send(cid, 'Your inventory filled up at ' + str(time_taken) + ' minutes.')
		db.setPlayer(sender, player, 0)
		send(cid, 'You got items, check your inventory (placeholder until i add shit)')
	def eat(self, psmg, sender, cid):
		playerExists(sender, cid)
		#5's to be replaced by nutrition_value from attr
		from items.item_classes import Container
		player = db.getPlayer(sender, 0)
		inv = player.inventory
		index = int(psmg[1]) - 1
		count = int(psmg[2])
		if (inv[index]['edible']):
			r = 0
			nutrition_value = inv[index]['nutrition-value']
			if (nutrition_value > 0):
				max_items = int((100 - player.hunger) / nutrition_value) #max items the player can consume
			else:
				max_items = count
			val_to_eat = min(count, max_items)
			if (val_to_eat < count):
				r = count - val_to_eat
			r += inv.rmByIndex(index, min(count, max_items))
			player.hunger += (count - r) * nutrition_value
			send(cid, 'You ate ' + str(count - r) + ' item(s) and gained ' + str((count - r) * nutrition_value) + ' nutrition.')
			db.setPlayer(sender, player, 0)
		else:
			send(cid, 'That is not a food item!')
	def pos(self, psmg, sender, cid):
		playerExists(sender, cid)
		from draw_map import draw_pos
		player = db.getPlayer(sender, 0)
		draw_pos(sender, player.pos, player.world)
		sendImage(cid, str(player.name) + ' is currently at ' + str(player.pos), 'data/players/' + str(sender) + '.png')
		return

	def resetbiomes(self, psmg, sender, cid):
		playerExists(sender, cid)
		if sender in mods:
			player = db.getPlayer(sender, 0)
			db.resetBiomes(player.world)
			send(cid, 'Biome resources reset successfully.')
		else:
			send(cid, 'You do not have permission to execute this command.')
	def resetinv(self, psmg, sender, cid):
		playerExists(sender, cid)
		from items.item_classes import Container
		player = db.getPlayer(sender, 0)
		player.inventory = Container(player.name + "'s inventory", 15)
		db.setPlayer(sender, player, 0)
		send(cid, 'Your inventory has been reset.')
	def me(self, psmg, sender, cid):
		playerExists(sender, cid)
		from items.item_classes import Container
		player = db.getPlayer(sender, 0)
		import numpy as np
		try:
			if (psmg[1] == '-p'):
				pass
		except:
			lb = np.array([[1, '\n', [None, None, None, None]]])
			m = np.array([[0, 'Here is some information about ' + player.name + ':', [None, None, None, None]]])
			m = np.concatenate((m, lb,
				toBar('Nutrition', player.hunger, 100, 20), lb,
				toBar('Hydration', player.thirst, 100, 20), lb,
				toBar('Health', player.health, 100, 20), lb,
				toBar('Stamina', player.exhaustion, 100, 20), lb,
				np.array([[0, 'Current position: ' + str(player.pos), [None, None, None, None]]]), lb,
				np.array([[0, 'Current biome: ' + str(db.getBiomeByID(player.biomeID, player.world).type), [None, None, None, None]]])
				),
			axis=0)
			sendRaw(cid, m.tolist())
	def maxstats(self, psmg, sender, cid):
		playerExists(sender, cid)
		player = db.getPlayer(sender, 0)
		player.hunger = 100
		player.thirst = 100
		player.health = 100
		player.exhaustion = 100
		send(cid, 'Your stats have been maxed.')
		db.setPlayer(sender, player, 0)

	def slashkill(self, psmg, sender, cid):
		playerExists(sender, cid)
		db.removePlayer(sender)
		sendRaw(cid, [[0, 'You died.', [1, None, None, None]]])

def send(cid, message):
	time.sleep(0.01) #prevent it from breaking
	print('>|' + str(cid) + '|' + str(message)) #keep
	sys.stdout.flush()
def sendImage(cid, message, img_path):
	time.sleep(0.01)
	print('$|' + str(cid) + '|' + str(message) + '|' + str(img_path)) #keep
	sys.stdout.flush()
def sendRaw(cid, message):
	import json
	time.sleep(0.01)
	print('^|' + str(cid) + '|' + json.dumps(message)) #keep
	sys.stdout.flush()

def toBar(name, val, max_val, bold_threshold):
	import math
	import numpy as np
	mult = 10 / max_val
	val_normalized = round(val * mult)
	max_normalized = max_val * mult
	m = np.zeros((3, 3)).tolist()
	m[0] = [0, name + ': ' + str(val) + '/' + str(max_val), [None, None, None, None]]
	if (val <= bold_threshold):
		m[0][2] = ([1, None, None, None])
	m[1] = [1, '\n', [None, None, None, None]]
	m[2] = [0, ('█' * val_normalized) + ('░' * (10 - val_normalized)), [None, None, None, None]]
	return np.array(m)

def playerExists(sender, cid):
	if db.isPlayer(sender):
		return
	else:
		send(cid, "You haven't created a player yet! Do !join <playername> <world>")
		exit()

try:
	cid = sys.argv[1]
	sender = sys.argv[2]
	psmg = sys.argv[3].split(",")
	msg = sys.argv[4]
except:
	cid = "[CHAT]"
	sender = "108791316110923750592"
	msg = input('message: ')
	if (msg == ''):
		msg = "!map"
	psmg = msg.split(' ')

handler = handler()
getattr(handler, psmg[0].split('!')[1].lower())(psmg, sender, cid)