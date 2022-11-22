from bridgeplotlib import *

if __name__ == "__main__":

    r1 = geometry_object.Rect(0, 75+1.27, 100, 1.27, name='top')  # top
    r2 = geometry_object.Rect(10, 75, 1.27, 75-1.27, id='folded-section',
              name='vertical-left')  # verticals
    r3 = geometry_object.Rect(90-1.27, 75, 1.27, 75-1.27,
              id='folded-section', name='vertical right')
    r4 = geometry_object.Rect(10+1.27, 75, 5, 1.27, id='folded-section',
              name='nib-left')  # lil nibs
    r5 = geometry_object.Rect(90-5-1.27, 75, 5, 1.27, id='folded-section', name='nib-right')
    r6 = geometry_object.Rect(10, 1.27, 80, 1.27, id='folded-section', name='bottom')  # bottom
    section = geometry_collection.GeometryCollection(
        (r1, r2, r3, r4, r5, r6), (('folded-section',),))

    r1 = geometry_object.Rect(0, 75+1.27, 100, 1.27)  # top
    r2 = geometry_object.Rect(10, 75, 1.27, 75-1.27)  # verticals
    r3 = geometry_object.Rect(90-1.27, 75, 1.27, 75-1.27)
    r4 = geometry_object.Rect(10+1.27, 75, 80-1.27 -
                              1.27, 75-1.27)  # solid section
    r5 = geometry_object.Rect(10, 1.27, 80, 1.27)  # bottom
    diaphragm = geometry_collection.GeometryCollection((r1, r2, r3, r4, r5))

    # diaphragm.display_geometry((120, 100), (6, 6), True)

    types = ('section', 'diaphragm', 'section', 'diaphragm', 'section')

    cross_sections = bridge.CrossSections(
        (section, diaphragm, section, diaphragm, section),
        ((0, 399.365), (399.365, 400.635), (400.635, 799.365),
         (799.365, 800.635), (800.635, 1200)),
        types
    )

    b = bridge.Bridge(1200, cross_sections)

    # display_max_flexural_stress(b, train.Train(100, 400))
    # display(b, 400, 10)
    # display_Q(section)
    print(section.find_Q(section.centroid))
    print(section.centroid)
    section.display_geometry()
