from bridgeplotlib import *

# Define the cross section geometry
r1 = geometry_object.Rect(
    0, 75+1.27, 100, 1.27, name='top', join_id='laminated')  # top
r2 = geometry_object.Rect(10, 75, 1.27, 75, id='folded-section',
                          name='vertical-left')  # verticals
r3 = geometry_object.Rect(90-1.27, 75, 1.27, 75,
                          id='folded-section', name='vertical-right')
r4 = geometry_object.Rect(10+1.27, 75, 5, 1.27, id='folded-section',
                          name='nib-left')  # lil nibs
r5 = geometry_object.Rect(90-5-1.27, 75, 5, 1.27,
                          id='folded-section', name='nib-right')
r6 = geometry_object.Rect(
    10+1.27, 1.27, 80-2*1.27, 1.27, id='folded-section', name='bottom')  # bottom
section = geometry_collection.GeometryCollection(
    (r1, r2, r3, r4, r5, r6), (('folded-section',), ('laminated',)), '')


# Create a diaphragm
r1 = geometry_object.Rect(0, 75+1.27, 100, 1.27)  # top
r2 = geometry_object.Rect(10, 75, 1.27, 75-1.27,
                          id='folded-section')  # verticals
r3 = geometry_object.Rect(90-1.27, 75, 1.27, 75-1.27, id='folded-section')
r4 = geometry_object.Rect(10+1.27, 75, 80-1.27 -
                          1.27, 75-1.27)  # solid section
r5 = geometry_object.Rect(
    10, 1.27, 80, 1.27, id='folded-section')  # bottom
diaphragm = geometry_collection.GeometryCollection(
    (r1, r2, r3, r4, r5), (('folded-section',),), name='diaphragm', ignore_thin_plate=True)


types = ('section', 'diaphragm', 'section', 'diaphragm', 'section')

cross_sections = bridge.CrossSections(
    (section, diaphragm, section, diaphragm, section),
    ((0, 399.365), (399.365, 400.635), (400.635, 799.365),
        (799.365, 800.635), (800.635, 1200)),
    types
)

b = bridge.Bridge(1200, cross_sections)

# section.display_geometry()
# diaphragm.display_geometry()


# solve_maximum_forces(b, 400, single_position=120) # train at center
# solve_maximum_forces(b, 400, single_position=0) # train at corner/start
solve_maximum_forces(b, 400, 1) # all possible positions
display_graphs((graph_max_flexural, graph_max_shear, graph_max_thin_plate_buckling,
               graph_max_thin_plate_shear), 2, 2, 4, b, 400, 1)
