from typing import List

import numpy as np
from gdpc import Block
from scipy.ndimage import gaussian_filter

import assignment.buildarea.helper as helper


class MapHolder:
    def __init__(self, ED, heights, ACCEPTABLE_BUILDING_SCORE=1.3):
        self.ED = ED
        self.heights = heights

        # CONSTANTS
        BUILD_AREA = ED.getBuildArea()  # BUILDAREA
        self.STARTX, self.STARTY, self.STARTZ = BUILD_AREA.begin
        self.LASTX, self.LASTY, self.LASTZ = BUILD_AREA.last
        self.SIZEX, self.SIZEY, self.SIZEZ = BUILD_AREA.size
        self.ACCEPTABLE_BUILDING_SCORE = ACCEPTABLE_BUILDING_SCORE
        # CENTERX = STARTX + (LASTX - STARTX) // 2
        # CENTERZ = STARTZ + (LASTZ - STARTZ) // 2

        self.building_places = np.zeros((self.SIZEX, self.SIZEZ))
        self.block_slope_score = np.zeros((self.SIZEX, self.SIZEZ))
        self.tree_spots = np.zeros((self.SIZEX, self.SIZEZ), dtype=bool)

    def find_flat_areas_and_trees(self, print_colors=False):
        SIZEX, SIZEY, SIZEZ = self.SIZEX, self.SIZEY, self.SIZEZ
        STARTX, STARTY, STARTZ = self.STARTX, self.STARTY, self.STARTZ
        LASTX, LASTY, LASTZ = self.LASTX, self.LASTY, self.LASTZ

        self.block_slope_score = np.zeros((SIZEX, SIZEZ))
        self.tree_spots = np.zeros((SIZEX, SIZEZ), dtype=bool)
        for x in range(STARTX, LASTX + 1):
            for z in range(STARTZ, LASTZ + 1):
                height_current_block = self.heights[(x - STARTX, z - STARTZ)]
                score_current_block = 0
                if helper.is_tree(self.ED, x, height_current_block, z):
                    self.tree_spots[x - STARTX, z - STARTZ] = True
                    self.block_slope_score[x - STARTX, z - STARTZ] = 1
                    continue
                if helper.is_water(self.ED, x, height_current_block, z):
                    self.block_slope_score[x - STARTX, z - STARTZ] = 10

                else:
                    neighbour_list = [
                        (x - STARTX + 1, z - STARTZ),
                        (x - STARTX - 1, z - STARTZ),
                        (x - STARTX, z - STARTZ + 1),
                        (x - STARTX, z - STARTZ - 1),
                    ]
                    for x_neighbour, z_neighbour in neighbour_list:
                        try:
                            neighbour_height = self.heights[(x_neighbour, z_neighbour)]
                            if not helper.is_tree(self.ED, x + 1, neighbour_height, z):
                                score_current_block += np.absolute(
                                    height_current_block - neighbour_height
                                )
                            else:
                                score_current_block += 1
                        except:
                            # border punishment
                            score_current_block += 10

                    self.block_slope_score[x - STARTX, z - STARTZ] = score_current_block

        self.block_slope_score = gaussian_filter(self.block_slope_score, sigma=3, mode="constant")

        if print_colors:
            for x in range(STARTX + 1, LASTX):
                for z in range(STARTZ + 1, LASTZ):
                    height_current_block = self.heights[(x - STARTX, z - STARTZ)] - 1
                    score = self.block_slope_score[x - STARTX, z - STARTZ]
                    if score > 7:
                        self.ED.placeBlock((x, height_current_block, z), Block("red_wool"))
                    elif score > 5:
                        self.ED.placeBlock((x, height_current_block, z), Block("pink_wool"))
                    elif score > 3:
                        self.ED.placeBlock((x, height_current_block, z), Block("yellow_wool"))
                    elif score > self.ACCEPTABLE_BUILDING_SCORE:
                        self.ED.placeBlock((x, height_current_block, z), Block("blue_wool"))
                    else:
                        self.ED.placeBlock((x, height_current_block, z), Block("green_wool"))
        return self.block_slope_score, self.tree_spots

    def claim_zone(self, xstart, zstart, sizex, sizez, door, size_edges):
        edges = 9
        for x in range(xstart - self.STARTX - edges, xstart + sizex - self.STARTX + edges):
            for z in range(zstart - self.STARTZ - edges, zstart + sizez - self.STARTZ + edges):
                try:
                    if self.building_places[x, z] == 0:
                        self.building_places[x, z] = 10_000
                except:
                    pass

        for x in range(xstart - self.STARTX - 1, xstart + sizex - self.STARTX + 2):
            for z in range(zstart - self.STARTZ - 1, zstart + sizez - self.STARTZ + 2):
                try:
                    self.building_places[x, z] = 20_000
                except:
                    pass

        # update slope score map, so we don't build there again
        self.block_slope_score += self.building_places
        return

    # recursively check reachable spots
    def check_reachable_spots(
        self, x, y, reachable_spots, best_loc_x, best_loc_z, best_loc_y, distance_area_look
    ):
        # Check if the spot has already been visited
        if (x, y) in reachable_spots:
            return reachable_spots
        elif len(reachable_spots) > 18:
            return reachable_spots

        # Check if the spot is reachable
        if self.is_spot_reachable(x, y, best_loc_x, best_loc_z, best_loc_y, distance_area_look):
            # Add the spot to the reachable spots array
            reachable_spots.append((x, y))

            # Check the neighbours of the spot recursively
            reachable_spots = self.check_reachable_spots(
                x - 1, y, reachable_spots, best_loc_x, best_loc_z, best_loc_y, distance_area_look
            )  # Check left neighbour
            reachable_spots = self.check_reachable_spots(
                x + 1, y, reachable_spots, best_loc_x, best_loc_z, best_loc_y, distance_area_look
            )  # Check right neighbour
            reachable_spots = self.check_reachable_spots(
                x, y - 1, reachable_spots, best_loc_x, best_loc_z, best_loc_y, distance_area_look
            )  # Check top neighbour
            reachable_spots = self.check_reachable_spots(
                x, y + 1, reachable_spots, best_loc_x, best_loc_z, best_loc_y, distance_area_look
            )  # Check bottom neighbour

        return reachable_spots

    # check if a spot is suitable to build
    def is_spot_reachable(self, x, y, best_loc_x, best_loc_z, best_loc_y, distance_area_look):
        reachable = True
        edge_dist = int((distance_area_look - 1) / 2)
        corners = [
            [edge_dist, edge_dist],
            [edge_dist, -edge_dist],
            [-edge_dist, edge_dist],
            [-edge_dist, -edge_dist],
        ]
        for cor_x, cor_y in corners:
            middle_x = best_loc_x + distance_area_look * x + cor_x
            middle_y = best_loc_z + distance_area_look * y + cor_y
            if 0 < middle_x < self.SIZEX and 0 < middle_y < self.SIZEZ:
                if not (best_loc_y - 2 <= self.heights[middle_x, middle_y] <= best_loc_y + 2):
                    reachable = False
                if not (
                    self.block_slope_score[middle_x, middle_y] < self.ACCEPTABLE_BUILDING_SCORE
                ):
                    reachable = False
            else:
                reachable = False
        return reachable

    def find_spot(self, best_loc_x, best_loc_y, best_loc_z, size):
        # Define the array of reachable spots
        reachable_spots = []
        # Check the reachable spots from the starting point
        reachable_spots = self.check_reachable_spots(
            0, 0, reachable_spots, best_loc_x, best_loc_z, best_loc_y, size
        )

        # Print the reachable spots
        if reachable_spots == []:
            reachable_spots.append([0, 0])

        translated_coords = []
        min_x = min(x for x, y in reachable_spots)
        min_y = min(y for x, y in reachable_spots)

        if min_x > 0:
            min_x = 0
        if min_y > 0:
            min_y = 0

        for x, y in reachable_spots:
            translated_coords.append((x - min_x, y - min_y))

        grid_x = max(x for x, y in translated_coords) + 1
        grid_y = max(y for x, y in translated_coords) + 1
        grid: List[List[int]] = [[0] * grid_y for _ in range(grid_x)]

        for x, y in translated_coords:
            grid[x][y] = 1

        for row in grid:
            print(row)

        return best_loc_x + size * min_x, best_loc_z + size * min_y, grid
