from glm import ivec2, ivec3
from gdpc import Block, Editor, Transform

def remove_trees(ED, xstart, ystart, zstart, sizex, sizey, sizez):
    removed_tree_blocks = []
    borderxz = 2
    bordery = 10
    for x in range(xstart - borderxz, xstart + sizex + borderxz + 1):
        for y in range(ystart, ystart + sizey + bordery):
            for z in range(zstart - borderxz, zstart + sizez + borderxz + 1):
                type = ED.getBlock((x, y, z))
                if ("leaves" in type.id or "log" in type.id or "wood" in type.id):
                    ED.placeBlock((x, y, z), Block("air"))
                    removed_tree_blocks.append((x, y, z))

    # todo: these neighbours do leave some artifacts of trees, but all corners
    #  often results in requesting blocks that are off the map. Remove the artifacts,
    #  or make map bigger, but this seems harder.

    neighbour_pos = [ivec3(1, 0, 0), ivec3(-1, 0, 0), ivec3(0, 1, 0), ivec3(0, -1, 0), ivec3(0, 0, 1), ivec3(0, 0, -1)]

    while len(removed_tree_blocks) > 0:
        block = removed_tree_blocks[0]
        removed_tree_blocks.pop(0)

        for np in neighbour_pos:
            neighbor_block = block + np
            type = ED.getBlock(neighbor_block)
            if ("leaves" in type.id or "log" in type.id or "wood" in type.id):
                ED.placeBlock(neighbor_block, Block("air"))
                removed_tree_blocks.append(neighbor_block)

def build_exterior_one_house_part(ED, sizex, sizey, sizez, ylevel, height):
    # outline
    for x in range(0, sizex):
        ED.placeBlock((x, ylevel+2, 0), Block("red_wool"))
        ED.placeBlock((x, ylevel+2, sizez-1), Block("red_wool"))

    for z in range(0, sizez):
        ED.placeBlock((0, ylevel+2 , z), Block("red_wool"))
        ED.placeBlock((sizex-1, ylevel+2, z), Block("red_wool"))