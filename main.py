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
	def fullmap(self, psmg, sender, cid):
		if (sender in mods):
			sendImage(cid, 'world map', db.getMapDir(db.getPlayerWorld(sender)))
		else:
			send(cid, 'You do not have permission to execute this command.')
		return
	def map(self, psmg, sender, cid):
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
	def travel(self, psmg, sender, cid):
		import numpy as np
		player = db.getPlayer(sender, 0)
		pcoords = db.getPlayer(sender, 1)
		from misc import find_endpoint, find_uncovered
		f_c = find_endpoint(psmg[1], float(psmg[2]), player.pos)
		if (f_c == -1):
			send(cid, 'That coordinate is out of bounds!')
			return
		send(cid, str(player.name) + ' travelled to ' + str(f_c))
		
		newcoords = find_uncovered(player.pos, f_c)

		player.pos = f_c
		player.biomeID = db.getIDofPos(player.pos, player.world)

		db.setPlayer(sender, np.concatenate((pcoords, newcoords)), 1)
		db.setPlayer(sender, player, 0)
	def gather(self, psmg, sender, cid):
		from map.classes import biome, itemID
		import configparser
		from resources import generateResources, calculateLoot
		itemnames = itemID()
		player = db.getPlayer(sender, 0)
		p_biome = db.getBiomeByID(player.biomeID, player.world)
		if (int(psmg[1]) > 1440):
			send(cid, 'You can only gather resources for up to 1 day (1440 minutes).')
			return
		if (type(p_biome.resources) == type(-1)):
			p_biome = generateResources(p_biome)
		loot, p_biome = calculateLoot(p_biome, psmg[1], 'damascus blade')
		db.updateBiomeByID(player.biomeID, player.world, p_biome)
		message = [[0, 'You gathered resources for ' + str(psmg[1]) + ' minutes and recieved:']]
		for i in range(0, loot.shape[0]):
			if (loot[i, 1] != 0):
				message.append([1, '\n'])
				message.append([0, itemnames[int(loot[i, 0])], [1, None, None, None]])
				message.append([0, ': '])
				message.append([0, str(int(loot[i, 1])), [1, None, None, None]])
		sendRaw(cid, message)

	def pos(self, psmg, sender, cid):
		from draw_map import draw_pos
		player = db.getPlayer(sender, 0)
		draw_pos(sender, player.pos, player.world)
		sendImage(cid, str(player.name) + ' is currently at ' + str(player.pos), 'data/players/' + str(sender) + '.png')
		return
	def worldlist(self, psmg, sender, cid):
		send(cid, db.worldList())
		return
	def resetbiomes(self, psmg, sender, cid):
		if sender in mods:
			player = db.getPlayer(sender, 0)
			db.resetBiomes(player.world)
			send(cid, 'Biome resources reset successfully.')
		else:
			send(cid, 'You do not have permission to execute this command.')
	def test(self, psmg, sender, cid):
		message = [[0, 'You gathered resources for ' + str(psmg[1]) + ' minutes and recieved:', [1, None, None, None]]]
		sendRaw(cid, message)

def send(cid, message):
	time.sleep(0.01) #prevent it from breaking
	print('>|' + str(cid) + '|' + str(message))
	sys.stdout.flush()
def sendImage(cid, message, img_path):
	time.sleep(0.01)
	print('$|' + str(cid) + '|' + str(message) + '|' + str(img_path))
	sys.stdout.flush()
def sendRaw(cid, message):
	import json
	time.sleep(0.01)
	print('^|' + str(cid) + '|' + json.dumps(message))
	sys.stdout.flush()

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
getattr(handler, psmg[0].split('!')[1])(psmg, sender, cid)



