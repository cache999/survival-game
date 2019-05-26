#generates default config file.
import configparser
#implement comments
configparser.ConfigParser.add_comment = lambda self, section, option, value: self.set(section, '# '+option, value)
config = configparser.ConfigParser()

config.add_section('min_size')
config.set('min_size', 'rm_small_biomes', '1')
config.add_comment('min_size', "All biomes will be kept if this is set to 0. Probably a bad idea because small biomes are pretty useless and clutter up the map with names. Default", '1')

config.set('min_size', 'deep_ocean_min', '50')
config.set('min_size', 'shallow_ocean_min', '30')
config.set('min_size', 'coral_reef_min', '5')
config.set('min_size', 'kelp_forest_min', '10')
config.set('min_size', 'ice_min', '20')
config.set('min_size', 'tiaga_min', '20')
config.set('min_size', 'tundra_min', '20')
config.set('min_size', 'sand_beach_min', '15')
config.set('min_size', 'steppe_min', '20')
config.set('min_size', 'plains_min', '20')
config.set('min_size', 'forest_min', '20')
config.set('min_size', 'swamp_min', '20')
config.set('min_size', 'desert_min', '20')
config.set('min_size', 'savanna_min', '20')
config.set('min_size', 'rainforest_min', '20')
config.set('min_size', 'mountain_min', '45')
config.set('min_size', 'river_min', '0')


config.add_section("res_max")
config.add_comment('res_max', "Defines the maximum amount of resources accessible in one pixel of a biome. Rounds up to 1. Remember that 1 pixel", "100m^2.")
config.set('res_max', '5', '0:1,33:100')
config.set('res_max', '6', '0:1,1:50,2:8,3:12,7:8,15:8,16:0.01,24:0.1,27:1')
config.set('res_max', '7', '0:1,4:2,7:4,8:3,9:3,24:0.05')
config.set('res_max', '8', '0:1,22:0.3,30:1,29:100')
config.set('res_max', '9', '0:1,3:6,4:3,7:6,35:0.00001')
config.set('res_max', '10', '0:1,7:100,11:4')
config.set('res_max', '11', '0:1,1:50,2:8,3:12,7:8,8:1,23:0.1,28:3')
config.set('res_max', '12', '0:1,1:3,2:8,3:9,6:1,8:8,9:4,')
config.set('res_max', '13', '0:1,5:0.5,21:0.5,29:100,34:0.07')
config.set('res_max', '14', '0:1,1:3,2:6,3:6,7:6,12:0.1,13:0.1,14:1')
config.set('res_max', '15', '0:1,1:50,2:8,3:8,23:1,25:1.68,28:1')


config.add_section('res_search')
config.add_comment('res_search', "Defines what item will be found every 1 minute of searching. Syntax: item:weight:qty:tool_needed. Rounds up to 1. Remember that 1 pixel", "100m^2.")
config.set('res_search', '5', '0:80:0:none,33:19:1:none,24:1:1:none')
config.set('res_search', '6', '0:202.8:0:none,1:1:1:none,2:60:1:none,3:60:1:none,7:40:3:none,15:5:1:none,16:0.1:16:none,24:0.5:1:none,27:5:12:none')
config.set('res_search', '7', '0:157:0:none,7:30:3:none,8:4:1:none,9:1:1:none,24:0.25:1:none')
config.set('res_search', '8', '0:50:0:none,22:1:4:none,29:48:1:none,30:1:1:none')
config.set('res_search', '9', '0:6998:0:none,3:1750:1:none,4:500:1:none,7:750:3:none,35:2:1:none')
config.set('res_search', '10', '0:50:0:none,7:40:4:none,11:10:2:none')
config.set('res_search', '11', '0:185.5:0:none,1:1:1:none,2:60:1:none,3:60:1:none,7:60:3:none,8:1:1:none,23:0.5:1:none,28:3:1:none')
config.set('res_search', '12', '0:102:0:none,1:1:1:none,2:20:1:none,3:20:1:none,6:4:16:none,8:8:1:none,9:40:1:none,17:1:4:none,18:1:4:none,19:19:1:none,20:1.9:1:none,25:2.9:1:none,31:20:1:none,32:0.1:1:none')
config.set('res_search', '13', '0:1159:0:none,5:20:1:none,21:20:1:none,29:300:1:none,34:1:1:none')
config.set('res_search', '14', '0:163:0:none,1:1:1:none,2:30:1:none,3:25.8:1:none,7:30:3:none,12:0.1:5:none,13:0.1:4:none,14:1:1:none')
config.set('res_search', '15', '0:219:0:none,1:4:1:none,2:120:1:none,3:120:1:none,23:8:1:none,26:8:1:none,28:8:1:none')


with open('map/biomes.cfg', 'w') as configfile:
    config.write(configfile)
print('updated config')