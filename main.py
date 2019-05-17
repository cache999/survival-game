import sys
import time
from data_handler import database
import threading
db = database()
promises = []

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
	pass

class handler:
	def newcharacter(self, psmg, sender, cid): 
		#create new char TODO: add confirmation
		if (len(psmg) == 1):
			send(cid, 'fuck you , please specify name and world')
		elif (len(psmg) == 2):
			send(cid, 'fuck you, please specify world')
		else:
			if (db.isWorld(psmg[2])):
				import copy
				character = char()
				character.world = psmg[2]
				character.name = psmg[1]
				character.head = -1
				character.chest = -1
				character.back = -1
				character.rh = -1
				character.lh = -1
				character.inventory = -1
				character.hunger = 75
				character.thirst = 75
				character.health = 100
				character.exhaustion = 0 #int between 0 and 100
				character.age = 0
				db.setPlayer(sender, copy.deepcopy(character))
				send(cid, 'Your character ' + psmg[1] + ' has been created!')
			else:
				send(cid, 'fuck you, ' + psmg[2] +' isnt an existing world')
	def newworld(self, psmg, sender, cid):
		if (len(psmg) > 1):
			from map.mapgen import gen_map
			gen_map(psmg[1])
		else:
			send(cid, 'Please provide a name!')
			return
		send(cid, 'The world has been created!')



def new_promise(command, sender, cid):
	for i in range(0, len(promises)):
		if (promises[i].snd == sender and promises[i].cmd == command and promises[i].cid == cid):
			promises[i].delete()
			return True
	promises.append(promise(command, sender, cid))
	send(cid, 'Please type the command again to confirm. The command will expire in 120 seconds.')



def send(cid, message):
	time.sleep(0.01) #prevent it from breaking
	print(str(cid) + '|' + str(message))
	sys.stdout.flush()

try:
	cid = sys.argv[1]
	sender = sys.argv[2]
	psmg = sys.argv[3].split(",")
	msg = sys.argv[4]

except:
	cid = "chatid"
	sender = "123test"
	msg = "!newworld benzou"
	psmg = msg.split(' ')


handler = handler()
getattr(handler, psmg[0].split('!')[1])(psmg, sender, cid)



