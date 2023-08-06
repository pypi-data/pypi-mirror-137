from bubblebuster import *
pbc=water_box_properties("test.pdb")
if not pbc.empty_cubes:
    print(True)
