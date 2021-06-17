#This isn't meant to be run from anything, instead it should run every time ItemIdMap is updated.
def UpdateItemNameMap():
	import json
	new_dict = {}
	with open('ItemIdMap.json') as id_dict:
		id_dict = json.load(id_dict).items()
	for key, val in id_dict:
		for key_n, val_n in val.items():
			new_dict.update({val_n: {'cat': key, 'id': key_n}})
	with open('ItemNameMap.json', 'w') as outfile:  
   		json.dump(new_dict, outfile)
if __name__ == "__main__":
	UpdateItemNameMap()
	print('done')