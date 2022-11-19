from bridgeplotlib import *

if __name__ == "__main__":

    r1 = geometry_object.Rect(0, 75+1.27, 100, 1.27)  # top
    r2 = geometry_object.Rect(10, 75, 1.27, 75-1.27)  # verticals
    r3 = geometry_object.Rect(90-1.27, 75, 1.27, 75-1.27)
    r4 = geometry_object.Rect(10+1.27, 75, 5, 1.27)  # lil nibs
    r5 = geometry_object.Rect(90-5-1.27, 75, 5, 1.27)
    r6 = geometry_object.Rect(10, 1.27, 80, 1.27)  # bottom
    section = geometry_collection.GeometryCollection(
        (r1, r2, r3, r4, r5, r6))

    r1 = geometry_object.Rect(0, 75+1.27, 100, 1.27)  # top
    r2 = geometry_object.Rect(10, 75, 1.27, 75-1.27)  # verticals
    r3 = geometry_object.Rect(90-1.27, 75, 1.27, 75-1.27)
    r4 = geometry_object.Rect(10+1.27, 75, 80-1.27 -
                              1.27, 75-1.27)  # solid section
    r5 = geometry_object.Rect(10, 1.27, 80, 1.27)  # bottom
    diaphragm = geometry_collection.GeometryCollection((r1, r2, r3, r4, r5))

    # diaphragm.display_geometry((120, 100), (6, 6), True)

    cross_sections = bridge.CrossSections(
        (section, diaphragm, section, diaphragm, section),
        ((0, 399.365), (399.365, 400.635), (400.635, 799.365),
         (799.365, 800.635), (800.635, 1200))
    )

    b = bridge.Bridge(1200, cross_sections)

    display_max_flexural_stress(b, train.Train(100, 400))
    # display(b, 400, 10)
