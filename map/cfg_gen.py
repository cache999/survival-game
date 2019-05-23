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

config.add_section('res_max')
config.add_comment('res_max', "Defines the maximum amount of resources accessible in one pixel of a biome. Rounds up to 1. Remember that 1 pixel", "100m^2.")
config.set('res_max', '11', '1:1,5:0.1,6:1')
config.set('res_max', '14', '1:0.5,7:0.1')
config.set('res_max', '9', '2:2,3:1,4:0.0001')

config.add_section('res_search')
config.add_comment('res_search', "Defines what item will be found every 1 minute of searching. Syntax: item:weight:qty:tool_needed. Rounds up to 1. Remember that 1 pixel", "100m^2.")
config.set('res_search', '11', '1:10:1:none,5:1:1:none,6:5:3:none')
config.set('res_search', '14', '1:3:1:none,7:0.1:1:none,6:3:3:none')
config.set('res_search', '9', '2:2:3:none,3:1:1:none,4:0.005:1:none')



with open('map/biomes.cfg', 'w') as configfile:
    config.write(configfile)
print('updated config')