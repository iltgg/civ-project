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
solve_maximum_forces(b, 400, single_position=0) # train at corner/start
# solve_maximum_forces(b, 400, 1)  # all possible positions

intermediate = True
if intermediate:
    print(f'centroid: {section.centroid:.3f}')
    print(f'I: {section.I:.3f}')
    print(f'V max: {max(maximum_shear_forces):.3f} | ratio of P: {max(maximum_shear_forces)/400:.3f}')
    print(f'M max: {max(maximum_bending_moments):.3f} | ratio of P: {max(maximum_bending_moments)/400:.3f}')
    print(f'Q glue: {section.find_Q(75):.3f}')
    print(f'b glue: {section.get_joint_width(section.get_joint_heights()[0]):.3f}')
    print(f'Q centroid: {section.find_Q(section.centroid):.3f}')
    print(f'b centroid: {section.find_width(section.centroid):.3f}')
    print(f'k=0.425 t: {section.side_flange[0][1]:.3f}, b: {section.side_flange[0][0]:.3f}')
    a = b.cross_sections.get_cross_section_bounds(section)[0]
    print(f'k=5 t: {section.side_shear[0][1]:.3f}, h: {section.side_shear[0][0]:.3f}, a: {a[1]-a[0]+0.635:.3f}')
    print(f'k=6 t: {section.vertical_flange[0][1]:.3f}, b: {section.vertical_flange[0][0]:.3f}')
    print(f'k=4 t: {section.top_flange[0][1]:.3f}, b: {section.top_flange[0][0]:.3f}')

display_graphs((graph_max_flexural, graph_max_shear, graph_max_thin_plate_buckling,
               graph_max_thin_plate_shear), 2, 2, 4, b, 400, 1)
