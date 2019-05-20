    
class biome:
	def __init__(self, type_):
		self.type = type_
		self.coords = []
	def addc(self, coord):
		self.coords.append(coord)

class world():
    def __init__(self, name):
        self.players = []
        self.name = name

def colours(): #mainly an easy way to modify colours
	return [
    [0, 0, 0],
    [0, 163, 204], #deep ocean
    [0, 184, 230], #Shallow_ocean
    [255, 167, 142], #Coral_reef
    [45, 71, 13], #Kelp_forest //updated
    [153, 229, 253], #Ice
    [8, 48, 0], #Taiga //updated
    [247, 192, 163], #Tundra //updated
    [255, 255, 153], #sand
    [185, 201, 106], #Steppe //updated
    [92, 214, 102], #Plains //updated
    [12, 109, 20], #Forest //updated
    [28, 51, 30], #Swamp //updated
    [237, 235, 128], #Desert //updated
    [177, 216, 78], #Savanna //updated
    [22, 226, 32], #Rainforest //updated
    [77, 77, 77], #Mountain
    [230, 255, 255], #Snow_mountain
    [166,252,252] #river
    ]