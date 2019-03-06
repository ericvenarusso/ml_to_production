from mongo import Mongo

"""
Droping the collections if exists
"""
for collection in ["train", "test", "target_map", "models", "results"]:
    Mongo().drop(collection) 

"""
Inserting CSV files into MongoDB
"""
Mongo().insert_csv('train.csv', ['id', 'bone_length', 'rotting_flesh', 'hair_length', 'has_soul', 'color', 'type'], 'train')
Mongo().insert_csv('test.csv', ['id', 'bone_length', 'rotting_flesh', 'hair_length', 'has_soul', 'color'], 'test')
Mongo().insert_one('target_map', {"Ghoul": 0, "Goblin": 1, "Ghost": 2})