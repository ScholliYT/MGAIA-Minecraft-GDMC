import requests
from glm import ivec3

def spawn_villager(coordinates: ivec3, villager_type: str = "minecraft:plains", custom_name: str = None, other_data: str = ""):
    url = 'http://127.0.0.1:9000/entities?x=%d&y=%d&z=%d'%(coordinates.x, coordinates.y, coordinates.z)

    data = [
        {
            'id': 'villager',
            'x': "~0.5",
            'y': "~0.0",
            "z": "~0.5",
            "data": "{%sVillagerData:{type:\"%s\"}%s}"%("CustomName:'{\"text\":\"" + custom_name + "\"}'," if custom_name else '', villager_type, other_data)
        }
    ]

    return requests.put(url, json=data)

def spawn_animal(coordinates: ivec3, animal: str, custom_data: str = ""):
    url = 'http://127.0.0.1:9000/entities?x=%d&y=%d&z=%d'%(coordinates.x, coordinates.y, coordinates.z)

    data = [
        {
            'id': animal,
            'x': "~0.5",
            'y': "~0.0",
            "z": "~0.5",
            "data": custom_data
        }
    ]

    return requests.put(url, json=data)

def spawn_entity(coordinates: ivec3, data):
    url = 'http://127.0.0.1:9000/entities?x=%d&y=%d&z=%d'%(coordinates.x, coordinates.y, coordinates.z)

    return requests.put(url, data)