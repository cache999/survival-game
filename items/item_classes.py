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
		pass
	def __eq__(self, other):
		if (type(other) == int):
			return 1
		return ((self.cat == other.cat and self.id == other.id and self.attr == other.attr and other.count < other.attr['stack']))

class Container:
	def __init__(self):
		self.slots = 5
		self.items = np.zeros(self.slots, dtype=object)
		self.f = lambda obj, add: (min(obj.attr['stack'], obj.count + add), add - min(obj.attr['stack'], obj.count + add))
	def recieve(self, item):
		for i in range(0, self.slots):
			if (item == self.items[i]):
				if (item.count == 0):
					break
				self.items[i], item = self.appendToStack(self.items[i], item)
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
	cont = Container()
	print(cont.items)
	cont.recieve(Item('Wood', 1, 6, -1))
	for i in range(0, cont.slots):
		if (type(cont.items[i]) == int):
			print('blank')
		else:
			print(cont.items[i].count)
	cont.recieve(Item('Wood', 1, 32, -1))
	for i in range(0, cont.slots):
		if (type(cont.items[i]) == int):
			print('blank')
		else:
			print(cont.items[i].count)