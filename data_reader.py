#simple data reader
from data_handler import database
from map.classes import world
db = database()
print(db.getWorldData('alpha').players)