from mongo import Mongo

"""
    Faz o drop das colecoes
"""
for collection in ["train", "test", "target_map", "models", "results"]:
    Mongo().drop(collection) 

"""
    Faz a injestao dos csvs e de uma linha no MongoDB 
"""
Mongo().insert_csv('train.csv', ['id', 'bone_length', 'rotting_flesh', 'hair_length', 'has_soul', 'color', 'type'], 'train')
Mongo().insert_csv('test.csv', ['id', 'bone_length', 'rotting_flesh', 'hair_length', 'has_soul', 'color'], 'test')
Mongo().insert_one('target_map', {"Ghoul": 0, "Goblin": 1, "Ghost": 2})