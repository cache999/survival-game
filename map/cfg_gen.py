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

config.add_section('resources')
config.add_comment('resources', "Defines the amount of resources accessible in one pixel of a biome. Remember that 1 pixel", "100m^2.")
config.set('resources', 'forest', 'log:10:none')



with open('map/biomes.cfg', 'w') as configfile:
    config.write(configfile)
print('updated config')