class tile:
	def __init__(self, type_):
		self.type = type_
		self.tag = -1
	def addtag(self, tag):
		self.tag = tag

class biome:
	def __init__(self, type_, initcoord):
		self.type = type_
		self.coords = [initcoord]
	def addc(self, coord):
		self.coords.append(coord)