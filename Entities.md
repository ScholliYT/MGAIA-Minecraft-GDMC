# Entity spawning guide

## Using the methods

All methods require an `ivec3` to represent the coordinates of where the entity is spawned. These are used to generate the url for spawning the mob. Besides this, the PUT request made to the API requires a payload in the form of a json object, placed within a list (`[{}]`). A number of data points are required:

```
[
    {
        "id": minecraft id representing entity (pig, cow, etc.),
        "x": "~0.5",
        "y": "~0.0",
        "z": "~0.5",
    }
]
```

The addition of the 0.5's in the x and z coordinates are there to spawn the entity in the middle of the block, instead of on the edge.

An additional `data` entry can be added to the payload, which is a `str` containing any additional information that should be given to the entity (e.g. a custom name). A number of methods have been created to preprogram some of the payloads.

### Spawn Villager

Method for spawning a villager with a certain name and villager type.

Arguments:

- coordinates: `ivec3`. Representation of where the entity should be spawned.
- villager_type: `str`. Villager types can be found [here](https://minecraft.fandom.com/wiki/Villager#Villager_type). Changes appearance of villager.
- custom_name: `str`. Custom name that is displayed above the villagers head.
- other_data: `str`. String for adding additional entity data.

Returns: `Response` of PUT request

### Spawn Animal

Method for spawning an entity with a given entity ID. Perfect for spawning animals.

Arguments:

- coordinates: `ivec3`. Representation of where the entity should be spawned.
- animal: `str`. Entity id, like `pig`, `cow`, etc.
- custom_data: `str`. String for adding additional entity data.

Returns: `Response` of PUT request

### Spawn Entity

Generalized method for creating request with given payload.

Arguments:

- coordinates: `ivec3`. Representation of where the entity should be spawned.
- data: `str`. String for adding additional entity data.

Returns: `Response` of PUT request
