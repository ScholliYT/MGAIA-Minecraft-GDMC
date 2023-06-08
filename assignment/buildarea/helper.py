import random
from typing import List, Tuple

import numpy as np


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


def sample_good_location_idx(x: np.ndarray, size_struct: int, percentile=1.0) -> Tuple[int, int]:
    # add borders so we don't build outside of heightmap
    n = int(size_struct / 2 + 1)
    x[:n, :] = 10_000
    x[-n:, :] = 10_000
    x[:, :n] = 10_000
    x[:, -n:] = 10_000


    # Calculate the threshold for the lowest 1% of values
    threshold = np.percentile(x, percentile)
    # Find the coordinates where values are smaller than the threshold
    indices = np.where(x < threshold)
    # Create a list of (x, y) tuples from the indices
    coordinates: List[Tuple[int, int]] = list(zip(indices[0], indices[1]))
    # Randomly select a single coordinate pair
    random_coordinate = random.choice(coordinates)

    return random_coordinate
