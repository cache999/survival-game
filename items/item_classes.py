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
		self.cat = str(cat)
		self.id = int(id_)
		self.count = int(count) #items can be of any stack size when initiated, changed once they are added to any container.
		with open('items/ItemIdMap.json') as id_dict:
			self.name = json.load(id_dict)[self.cat][str(self.id)]
		if (type(attributes) == int):
			import os
			file = 'items/item_attributes/' + self.name.replace(" ", "") + '.json'
			if (os.path.isfile(file)):
				with open(file) as item_attr:
					self.attr = json.load(item_attr)
			else:
				self.attr = {}
		else:
			self.attr = {}
		if (self.attr.get('stack') == None):
			self.attr['stack'] = 99
	#def __str__(self):
	#	return 'fuk'
	def __eq__(self, other):
		return (self.cat == other.cat and self.id == other.id and self.attr == other.attr)
	def __bool__(self):
		#checks if the item is empty
		return not(self.cat == "Nothing")
	def __getitem__(self, key):
		return self.attr.get(key)

class Container:
	def __init__(self, name, slots):
		self.slots = slots
		self.items = np.full(self.slots, Item("Nothing", 1, 0, -1) ,dtype=object)
		self.name = name
	def recieve(self, item):
		#appends what it can to its own slots.
		#returns 0 if all were accepted, or the item if there was something left over.
		for i in range(0, self.slots):
			if ((item == self[i] and self[i].count < self[i].attr['stack']) or not(bool(self[i]))):
				if (item.count == 0):
					break
				self[i], item = self.appendToStack(self[i], item)
		if (item.count != 0):
			return item
		return 0
	def make_array(self):
		import json
		m = [[0, self.name, [1, None, None, None]], [0, ' has ' + str(self.slots) + ' slots and contains:']]
		for i in range(0, self.slots):
			m.append([1, '\n'])
			m.append([0, str(i+1) + ': '])
			if (bool(self[i])):
				m.append([0, self[i].name + ': ' + str(self[i].count)])
			else:
				m.append([0, '--'])
		return m
	def __add__(self, item):
		return self.recieve(item)
		#this looks cool
	def __str__(self):
		#shows info about it in terminal.
		m = self.name + ' has ' + str(self.slots) + ' slots and contains:\n'
		for i in range(0, self.slots):
			if (type(self[i]) == int):
				m = m + '<empty slot>\n'
			else:
				m = m + self[i].name + ': ' + str(self[i].count) + '\n'
		return m
	def transfer(self, index, cont):
		#tries to transfer an item to a different container.
		if (type(self[index]) == int):
			return 0
		self[index] = cont.recieve(self[index])
	def appendToStack(self, to, item):
		import copy
		if (not(bool(to))): #if empty:
			to = copy.deepcopy(item)
			to.count = min(item.attr['stack'], item.count)
			item.count = item.count - to.count
			return to, item
		else:			
			new_to = min(item.attr['stack'], to.count + item.count)
			item.count -= new_to - to.count
			to.count = new_to
			return to, item
	def rmByIndex(self, index, count):
		#remove will first try to remove from the least full stack, then in order from bottom right to top left.
		import json
		removed = min(int(count), self[index].count)
		self[index].count -= removed
		if (self[index].count == 0):
			self[index] = Item("Nothing", 1, 0, -1)
		return count - removed #remainder
	def getCat(self, index):
		return self[index].cat

	#i have no idea but these are
	def __getitem__(self, key):
		return self.items[key]
	def __setitem__(self, key, value):
		self.items[key] = value



'''
Container + Item
 - adds item to the container
Container1
'''
if __name__ == "__main__":
	cont1 = Container('benzou', 5)
	cont1 + Item('Wood', 1, 6, -1)
	print('added')
	print(cont1)
