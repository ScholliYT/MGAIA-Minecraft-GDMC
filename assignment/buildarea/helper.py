def is_water(ED, x, y, z):
    type = ED.getBlock((x, y - 1, z))
    water_specifiers = ["water", "lava", "ice"]
    return any([x in type.id for x in water_specifiers])


def is_tree(ED, x, y, z):
    type = ED.getBlock((x, y - 1, z))
    wood_specifiers = ["wood", "log"]
    return any([x in type.id for x in wood_specifiers])


def is_air(ED, x, y, z):
    type = ED.getBlock((x, y - 1, z))
    if "air" in type.id:
        return True
    return False


def find_min_idx(x, size_struct):
    # add borders so we don't build outside of heightmap
    n = int(size_struct / 2 + 1)
    x[:n, :] = 10_000
    x[-n:, :] = 10_000
    x[:, :n] = 10_000
    x[:, -n:] = 10_000

    # find min idx of map
    k = x.argmin()
    ncol = x.shape[1]
    return int(k / ncol), int(k % ncol)
