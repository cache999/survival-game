import sys
import time
from data_handler import database
import threading
db = database()
promises = []
mods = []
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

class char:
	def __init__(self, world, name):
		self.head = -1
		self.chest = -1
		self.back = -1
		self.rh = -1
		self.lh = -1
		self.inventory = -1
		self.hunger = 75
		self.thirst = 75
		self.health = 100
		self.exhaustion = 0 #int between 0 and 100
		self.age = 0
		self.world = world
		self.name = name
		self.pos = -1


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
				db.setWorld(-1, world_object, psmg[2])
			else:
				send(cid, 'fuck you, ' + str(psmg[2]) +' isnt an existing world')
	def complete_map(self, psmg, sender, cid):
		if (sender in mods):
			sendImage(cid, 'world map', db.getMapDir(db.getPlayerWorld(sender)))
		else:
			send(cid, 'You do not have permission to execute this command.')
	def map(self, psmg, sender, cid):
		from draw_map import draw_pos
		player = db.getPlayer(sender, 0)
		draw_pos(sender, player.pos, player.world)
		sendImage(cid, 'your current position', 'data/players/' + str(sender) + '.png')
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
		player = db.getPlayer(sender, 0)
		from misc import find_endpoint, find_uncovered
		f_c = find_endpoint(psmg[1], float(psmg[2]), player.pos)
		if (f_c == -1):
			send(cid, 'That coordinate is out of bounds!')
			return
		send(cid, 'You travelled to ' + str(f_c))
		player.pos = f_c
		db.setPlayer(sender, player, 0)
	def pos(self, psmg, sender, cid):
		send(cid, 'You are currently at ' + str(db.getPlayer(sender, 0).pos))
		return
	def worldlist(self, psmg, sender, cid):
		send(cid, db.worldList())
		return


def send(cid, message):
	time.sleep(0.01) #prevent it from breaking
	print('>|' + str(cid) + '|' + str(message))
	sys.stdout.flush()
def sendImage(cid, message, img_path):
	time.sleep(0.01)
	print('$|' + str(cid) + '|' + str(message) + '|' + str(img_path))
	sys.stdout.flush()

try:
	cid = sys.argv[1]
	sender = sys.argv[2]
	psmg = sys.argv[3].split(",")
	msg = sys.argv[4]
except:
	#for offline testing
	cid = "[CHAT]"
	sender = "108791316110923750592"
	msg = "!map"
	psmg = msg.split(' ')

handler = handler()
getattr(handler, psmg[0].split('!')[1])(psmg, sender, cid)



