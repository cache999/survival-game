'''
Catagories:
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
		self.name = 'Unknown Plant - Wetland' #id to name later
		self.count = count
		if (type(attributes) == int):
			with open('items/item_attributes/' + self.name.replace(" ", "") + '.json') as item_attr:
				self.attr = json.load(item_attr)
	def __str__(self):
		pass
	def __eq__(self, other):
		pass
class Character:
	def __init__(self): 
		#self.stuff = stuff
		pass

#i = Item('wood', 1, 7, -1)
