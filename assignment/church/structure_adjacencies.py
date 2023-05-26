import logging

from assignment.church.structures import (
    church_altar,
    churchcorner_altar_left,
    churchcorner_altar_right,
    churchcorner_straight,
    churchentrance,
    churchstraight_no_altar,
    churchstraight_to_altar,

    # roofs
    churchroof_altar,
    churchroof_corner,
    churchroof_entrance,
    churchroof_straight,
    empty_space_air,
)
from assignment.utils.structure_adjacency import StructureAdjacency, all_rotations, check_symmetry
from assignment.utils.structure_rotation import StructureRotation

logger = logging.getLogger(__name__)

structure_adjecencies = {
    empty_space_air: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=empty_space_air,
        x_minus=[
            *all_rotations(empty_space_air),
            StructureRotation(church_altar, 0),
            StructureRotation(church_altar, 2),
            StructureRotation(church_altar, 3),
            StructureRotation(churchcorner_altar_left, 2),
            StructureRotation(churchcorner_altar_left, 3),
            StructureRotation(churchcorner_altar_right, 0),
            StructureRotation(churchcorner_altar_right, 3),
            StructureRotation(churchcorner_straight, 0),
            StructureRotation(churchcorner_straight, 3),
            StructureRotation(churchentrance, 0),
            StructureRotation(churchentrance, 1),
            StructureRotation(churchentrance, 2),
            StructureRotation(churchstraight_no_altar, 0),
            StructureRotation(churchstraight_no_altar, 2),
            StructureRotation(churchstraight_to_altar, 0),
            StructureRotation(churchstraight_to_altar, 2),
            #roofs
            StructureRotation(churchroof_altar, 0),
            StructureRotation(churchroof_altar, 2),
            StructureRotation(churchroof_altar, 3),
            StructureRotation(churchroof_corner, 0),
            StructureRotation(churchroof_corner, 3),
            StructureRotation(churchroof_entrance, 0),
            StructureRotation(churchroof_entrance, 1),
            StructureRotation(churchroof_entrance, 2),
            StructureRotation(churchroof_straight, 0),
            StructureRotation(churchroof_straight, 2),
        ],
        
        z_plus=[
            *all_rotations(empty_space_air),
            StructureRotation(church_altar, 1),
            StructureRotation(church_altar, 2),
            StructureRotation(church_altar, 3),
            StructureRotation(churchcorner_altar_left, 1),
            StructureRotation(churchcorner_altar_left, 2),
            StructureRotation(churchcorner_altar_right, 2),
            StructureRotation(churchcorner_altar_right, 3),
            StructureRotation(churchcorner_straight, 2),
            StructureRotation(churchcorner_straight, 3),
            StructureRotation(churchentrance, 0),
            StructureRotation(churchentrance, 1),
            StructureRotation(churchentrance, 3),
            StructureRotation(churchstraight_no_altar, 1),
            StructureRotation(churchstraight_no_altar, 3),
            StructureRotation(churchstraight_to_altar, 1),
            StructureRotation(churchstraight_to_altar, 3),
            #roofs
            StructureRotation(churchroof_altar, 1),
            StructureRotation(churchroof_altar, 2),
            StructureRotation(churchroof_altar, 3),
            StructureRotation(churchroof_corner, 2),
            StructureRotation(churchroof_corner, 3),
            StructureRotation(churchroof_entrance, 0),
            StructureRotation(churchroof_entrance, 1),
            StructureRotation(churchroof_entrance, 3),
            StructureRotation(churchroof_straight, 1),
            StructureRotation(churchroof_straight, 3),
        ],
        x_plus=[
            *all_rotations(empty_space_air),
            StructureRotation(church_altar, 0),
            StructureRotation(church_altar, 1),
            StructureRotation(church_altar, 2),
            StructureRotation(churchcorner_altar_left, 0),
            StructureRotation(churchcorner_altar_left, 1),
            StructureRotation(churchcorner_altar_right, 1),
            StructureRotation(churchcorner_altar_right, 2),
            StructureRotation(churchcorner_straight, 1),
            StructureRotation(churchcorner_straight, 2),
            StructureRotation(churchentrance, 0),
            StructureRotation(churchentrance, 2),
            StructureRotation(churchentrance, 3),
            StructureRotation(churchstraight_no_altar, 0),
            StructureRotation(churchstraight_no_altar, 2),
            StructureRotation(churchstraight_to_altar, 0),
            StructureRotation(churchstraight_to_altar, 2),
            #roofs
            StructureRotation(churchroof_altar, 0),
            StructureRotation(churchroof_altar, 1),
            StructureRotation(churchroof_altar, 2),
            StructureRotation(churchroof_corner, 1),
            StructureRotation(churchroof_corner, 2),
            StructureRotation(churchroof_entrance, 0),
            StructureRotation(churchroof_entrance, 2),
            StructureRotation(churchroof_entrance, 3),
            StructureRotation(churchroof_straight, 0),
            StructureRotation(churchroof_straight, 2),
        ],

        z_minus=[
            *all_rotations(empty_space_air),
            StructureRotation(church_altar, 0),
            StructureRotation(church_altar, 1),
            StructureRotation(church_altar, 3),
            StructureRotation(churchcorner_altar_left, 0),
            StructureRotation(churchcorner_altar_left, 3),
            StructureRotation(churchcorner_altar_right, 0),
            StructureRotation(churchcorner_altar_right, 1),
            StructureRotation(churchcorner_straight, 0),
            StructureRotation(churchcorner_straight, 1),
            StructureRotation(churchentrance, 1),
            StructureRotation(churchentrance, 2),
            StructureRotation(churchentrance, 3),
            StructureRotation(churchstraight_no_altar, 1),
            StructureRotation(churchstraight_no_altar, 3),
            StructureRotation(churchstraight_to_altar, 1),
            StructureRotation(churchstraight_to_altar, 3),
            #roofs
            StructureRotation(churchroof_altar, 0),
            StructureRotation(churchroof_altar, 1),
            StructureRotation(churchroof_altar, 3),
            StructureRotation(churchroof_corner, 0),
            StructureRotation(churchroof_corner, 1),
            StructureRotation(churchroof_entrance, 1),
            StructureRotation(churchroof_entrance, 2),
            StructureRotation(churchroof_entrance, 3),
            StructureRotation(churchroof_straight, 1),
            StructureRotation(churchroof_straight, 3),
        ],
    ),
    church_altar: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=church_altar,
        z_minus=[
            StructureRotation(churchcorner_altar_left, 1),
            StructureRotation(churchcorner_altar_right, 3),
            StructureRotation(churchentrance, 0),
            StructureRotation(churchstraight_to_altar, 0),
        ],

        y_plus=[
            #roofs
            StructureRotation(churchroof_altar, 0),
        ]
    ),
     churchcorner_altar_left: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name= churchcorner_altar_left,
        
        x_plus=[
            StructureRotation(church_altar, 3),
            StructureRotation(churchstraight_to_altar, 3)
        ],

        z_minus=[
            StructureRotation(churchstraight_no_altar, 0)
        ],

        y_plus = [
            #roofs
            StructureRotation(churchroof_corner, 1)
        ]
    ),
    churchcorner_altar_right: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=churchcorner_altar_right,
        
        x_minus=[
            StructureRotation(church_altar, 1),
            StructureRotation(churchstraight_to_altar, 1)
        ],

        z_minus=[
            StructureRotation(churchentrance, 0),
            StructureRotation(churchstraight_no_altar, 0)
        ],

        y_plus = [
            #roofs
            StructureRotation(churchroof_corner, 0)
        ]
    ),

    churchcorner_straight: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=churchcorner_straight,
        x_minus=[
            StructureRotation(churchstraight_no_altar, 1),
            StructureRotation(churchstraight_to_altar, 1)
        ],
        
        z_minus=[
            StructureRotation(churchentrance, 0),
            StructureRotation(churchstraight_no_altar, 0)
        ],

        y_plus = [
            #roofs
            StructureRotation(churchroof_corner, 0)
        ]
    ),

    churchentrance: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=churchentrance,
        
        z_plus=[
            StructureRotation(church_altar, 0),
            StructureRotation(churchcorner_altar_right, 0),
            StructureRotation(churchcorner_straight, 0),
            StructureRotation(churchstraight_no_altar, 0),
            StructureRotation(churchstraight_to_altar, 0)
            
        ],
        y_plus = [
            #roofs
            StructureRotation(churchroof_entrance, 0)
        ]
    ),

    churchstraight_no_altar: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=churchstraight_no_altar,
        
        z_plus=[
            StructureRotation(churchcorner_altar_left, 0),
            StructureRotation(churchcorner_altar_right, 0),
            StructureRotation(churchcorner_straight, 0),
            StructureRotation(churchstraight_no_altar, 0),
            StructureRotation(churchstraight_to_altar, 0)
        ],

        z_minus=[
            StructureRotation(churchentrance, 0),
            StructureRotation(churchcorner_straight, 3),
            StructureRotation(churchstraight_no_altar, 0)
        ],

        y_plus = [
            #roofs
            StructureRotation(churchroof_straight, 0)
        ]
    ),

    churchstraight_to_altar: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=churchstraight_to_altar,
        
        z_plus=[
            StructureRotation(churchstraight_to_altar, 0),
            StructureRotation(church_altar, 0),
        ],

        z_minus=[
            StructureRotation(churchcorner_altar_left, 1),
            StructureRotation(churchcorner_altar_right, 3),
            StructureRotation(churchcorner_straight, 3),
            StructureRotation(churchentrance, 0),
            StructureRotation(churchstraight_no_altar, 0),
            StructureRotation(churchstraight_to_altar, 0)
        ],

        y_plus = [
            #roofs
            StructureRotation(churchroof_straight, 0),
        ]
    ),

    churchroof_altar: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=churchroof_altar,
        
        y_minus = [
            #roofs
            StructureRotation(church_altar, 0),
        ]
    ),

    churchroof_corner: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=churchroof_corner,
        
        y_minus = [
            #roofs
            StructureRotation(churchcorner_altar_left, 3),
            StructureRotation(churchcorner_altar_right, 0),
            StructureRotation(churchcorner_straight, 0)   
        ]
    ),

    churchroof_entrance: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=churchroof_entrance,
        
        y_minus = [
            #roofs
            StructureRotation(churchentrance, 0)
        ]
    ),

    churchroof_straight: StructureAdjacency(
        empty_space_air=empty_space_air,
        structure_name=churchroof_straight,
        
        y_minus = [
            #roofs
            StructureRotation(churchstraight_no_altar, 0),
            StructureRotation(churchstraight_to_altar, 0),
        ]
    )


}

if __name__ == "__main__":
    print(structure_adjecencies[church_altar].adjecent_structrues("z_minus", 3))

    check_symmetry(structure_adjecencies)