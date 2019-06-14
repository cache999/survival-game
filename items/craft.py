#attributes: -2 = any attribute
#attributes: -1 = default attributes
#time-type: waiting or crafting
'''
IN: Container containing items
1. items are hashed into a set of unique items (unique attributes)
2. items requested are matched with the set of unique items. Logic to determine which item(s) in the set are selected depending on if attributes need to be the same. If
there are no matches, add the item to the missing items list.
3. The candidates have their count summed (using the container array) to see if there are enough items. If there are, the items are deducted from the liszt. If there
are any instances where there aren't enough items, continue looping but record all instances of missing items into the missing items list.
4. Try to append back into the container. If cannot be appended, throw error
5. return container

EXAMPLE:
inv = [plant fibers, 3, custom_attr], [plant fibers, 3, default attr], [log, 8, default attr], [log, 7, default attr]
#unique = [plant fibers, custom attr], [plant fibers, default attr], [log, default attr]
np.argwhere([plant fibers, any attr]) --> 0, 1
repeat for reversed list:
try to deduct, if not, log the missing item in the missing list
repeat for other items if nessecary


'''
from items.item_classes import Item, Container
import numpy as np
from map.classes import char
class ItemReq:
	def __init__(self, cat, id_, count, attr):
		self.cat = cat
		self.id = id_
		self.count = count
		self.attr = attr
		
		if (type(self.attr) == int):
			if (self.attr == -1):
				self.attr == json.load(open('items/item_attributes/' + self.name.replace(" ", "") + '.json'))
				self.eq_type = 'hard'
			if (self.attr == -2):
				self.eq_type = 'soft'
		else:
			self.eq_type = 'hard'
#errors:
#1 = successful craft (+inven)
#-1 = not enough hunger
#-2 = invalid recipe
#-3 = not enough materials (+missing list)
#-4 = no space

def craft(cat, id_, amount, player):
	import json
	import copy
	player = copy.deepcopy(player)
	inv = player.inventory
	with open('items/recipes.json') as recipe:
		recipe = json.load(recipe).get(cat + ', ' + str(id_))
	if (recipe == None):
		return -2, -1 #not a valid recipe
	if (player.hunger <= int(recipe.get('hunger')) * int(amount)): #hunger too low
		return -1, -1

	recipe = recipe.get('requirements')
	#make reqs an array of ItemReq objects, init missing and req_idx
	reqs = list(map(lambda x: ItemReq(x[0], x[1], x[2] * amount, x[3]), recipe))
	reql = len(reqs)
	missing = np.zeros(reql)
	req_idx = []
	for i in range(0, reql):
		idx = np.argwhere(inv.items == reqs[i])
		if (idx.shape == 0):
			missing[i] = reqs[i][2] * amount
		else:
			req_idx.append(idx.flatten().tolist())
	for i in range(0, reql):
		needed = int(reqs[i].count)
		for j in reversed(req_idx[i]):
			#deduct the minimum of: the max stack size, the current count and the items remaining needed.
			deduct = min(int(inv[j]['stack']), int(inv[j].count), needed)
			needed -= deduct
			inv[j].count -= deduct
			if (needed == 0):
				break
		if (needed != 0):
			missing[i] = needed
	if (np.count_nonzero(missing) > 0):
		indices = np.nonzero(missing)
		item_counts = missing[indices]
		func = np.vectorize(lambda x, y: (0, str(json.load(open('items/ItemIdMap.json'))[recipe[x][0]][str(recipe[x][1])]) + ': ' + str(int(y))))

		names = np.zeros((reql, 2), dtype=object)

		names = np.array(func(indices, item_counts))
		names = names.T
		#names = func(indices, item_counts)
		linebreaks = np.vstack((np.full(reql, 1, dtype=object), np.full(reql, '\n'))).T

		message = np.zeros((reql * 2, 2), dtype=object)
		message[::2] = names
		message[1::2] = linebreaks
		message = np.insert(message, 0, [1, '\n'], axis=0)
		message = np.insert(message, 0, ['0', 'You are missing some materials required for the craft, listed below:'], axis=0)

		return (-3, message)
	else:
		#append crafted to inven
		r = inv + Item(cat, int(id_), amount, -1)
		if (type(r) != int):
			return -4, -1
		player.inventory = inv
		return 1, player
if __name__ == "__main__":
	c = char('idot', 'benzou')
	c.inventory + Item('Wood', 1, 1, -1)
	c.inventory + Item('Plants', 1, 12, -1)
	status, e = craft('Organic Materials', 1, 3, c)
	if (status == 1):
		c = e
	if (status == -1):
		print("you don't have enough nutrition")
	if (status == -2):
		print("invalid item!")
	if (status == -3):
		print("you don't have enough materials!")
		print(e.tolist())
	if (status == -4):
		print("your inventory doesn't have enough space!")
	#print(c.inventory)
	print(c.hunger)