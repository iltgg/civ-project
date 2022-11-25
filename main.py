from bridgeplotlib import *

if __name__ == "__main__":

    # Design 0

    r11 = geometry_object.Rect(0, 75+1.27*2, 100, 1.27,
                              name='top', join_id='laminated')  # top
    r1 = geometry_object.Rect(
        0, 75+1.27, 100, 1.27, name='top2', join_id='laminated')  # top
    r2 = geometry_object.Rect(10, 75, 1.27, 75-1.27, id='folded-section',
                              name='vertical-left')  # verticals
    r3 = geometry_object.Rect(90-1.27, 75, 1.27, 75-1.27,
                              id='folded-section', name='vertical-right')
    r4 = geometry_object.Rect(10+1.27, 75, 5, 1.27, id='folded-section',
                              name='nib-left')  # lil nibs
    r5 = geometry_object.Rect(90-5-1.27, 75, 5, 1.27,
                              id='folded-section', name='nib-right')
    r6 = geometry_object.Rect(
        10, 1.27, 80, 1.27, id='folded-section', name='bottom')  # bottom
    section = geometry_collection.GeometryCollection(
        (r1, r2, r3, r4, r5, r6), (('folded-section',), ('laminated',)), 'section')

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

    # diaphragm.display_geometry((120, 100), (6, 6), True)

    types = ('section', 'diaphragm', 'section', 'diaphragm', 'section')

    cross_sections = bridge.CrossSections(
        (section, diaphragm, section, diaphragm, section),
        ((0, 399.365), (399.365, 400.635), (400.635, 799.365),
         (799.365, 800.635), (800.635, 1200)),
        types
    )

    b = bridge.Bridge(1200, cross_sections)

    # for joint in diaphragm.get_joint_heights():
    #     print(joint)
    # print('---------------------')
    # diaphragm.display_geometry()

    # r1 = geometry_object.Rect(0, 100, 30, 100)

    # section = geometry_collection.GeometryCollection((r1,))

    # display_Q(section)

    # display_max_flexural_stress(b, train.Train(100, 400))
    # display(b, 400, 10)
    # print(section.find_Q(75))
    # print(section.find_Q(section.centroid))
    # for joint in section.get_joint_heights():
    #     print(joint)
    # diaphragm.display_geometry()
    # section.display_geometry()
    print(section.top_flange)
    print(section.side_flange)
    print(section.vertical_flange)
    print(section.side_shear)
    # section.display_geometry(show_joints=True)
    # display_Q(section)

    # print(b.get_board_amount()/10**6)

    
    
    solve_maximum_forces(b, 400, 10)
    
    display_graphs((graph_max_flexural, graph_max_shear, graph_max_thin_plate_buckling, graph_max_thin_plate_shear), 2, 2, 4, b, 400, 1)
    
    # print(max(maximum_bending_moments))

    # display_width(section)

    # display_maximum_forces(b)
    # diaphragm.display_geometry()