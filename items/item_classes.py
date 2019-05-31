import numpy as np
'''
Categories:
 - Wood
 - Vegetation
 - Food
 - 

'''
class Item:
	def __init__(self, cat, id_, count, attributes):
		import json
		#initialize a new item object
		self.cat = cat
		self.id = id_
		self.count = count #items can be of any stack size when initiated, changed once they are added to any container.
		with open('items/ItemIdMap.json') as id_dict:
			self.name = json.load(id_dict)[self.cat][str(self.id)]
		if (type(attributes) == int):
			import os
			file = 'items/item_attributes/' + self.name.replace(" ", "") + '.json'
			if (os.path.isfile(file)):
				with open(file) as item_attr:
					self.attr = json.load(item_attr)
			else:
				self.attr = {
				}
		if (self.attr.get('stack') == None):
			self.attr['stack'] = 99
	def __str__(self):
		return 'fuk'
	def __eq__(self, other):
		if (type(other) == int):
			return 1
		return ((self.cat == other.cat and self.id == other.id and self.attr == other.attr and other.count < other.attr['stack']))

class Container:
	def __init__(self, name, slots):
		self.slots = slots
		self.items = np.zeros(self.slots, dtype=object)
		self.name = name
	def recieve(self, item):
		#appends what it can to its own slots.
		#returns 0 if all were accepted, or the item if there was something left over.
		for i in range(0, self.slots):
			if (item == self.items[i]):
				if (item.count == 0):
					break
				self.items[i], item = self.appendToStack(self.items[i], item)
		if (item.count != 0):
			return item
		return 0
	def __str__(self):
		m = self.name + ' has ' + str(self.slots) + ' slots and contains:\n'
		for i in range(0, self.slots):
			if (type(self.items[i]) == int):
				m = m + '<empty slot>\n'
			else:
				m = m + self.items[i].name + ': ' + str(self.items[i].count) + '\n'
		return m
	def transfer(self, index, cont):
		#tries to transfer an item to a different container.
		if (type(self.items[index]) == int):
			return 0
		self.items[index] = cont.recieve(self.items[index])
	def appendToStack(self, to, item):
		import copy
		if (type(to) == int):
			to = copy.deepcopy(item)
			to.count = min(item.attr['stack'], item.count)
			item.count = item.count - to.count
			return to, item
		else:			
			new_to = min(item.attr['stack'], to.count + item.count)
			item.count -= new_to - to.count
			to.count = new_to
			return to, item
if __name__ == "__main__":
	cont1 = Container('benzou', 5)
	wood = Item("Wood", 1, 39, -1)
	cont1.recieve(wood)
	print(cont1)

	cont2 = Container('bigger benzou', 15)
	cont1.transfer(2, cont2)
	print(cont1)
	print(cont2)

	cont1.recieve(Item("Unknown", 3, 9, -1))
	cont2.transfer(1, cont1)

	print(cont1)
	print(cont2)

