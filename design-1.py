from bridgeplotlib import *

x = 1.27
h = 100

top = geometry_object.Rect(0, h+x, 100, x, name='top')
vertical_left = geometry_object.Rect(
    11.865, h, 1.27, h, name='vertical left', id='bottom')
vertical_right = geometry_object.Rect(
    86.865, h, 1.27, h, name='vertical right', id='bottom')
flange_left = geometry_object.Rect(
    13.135, h, 36.865, 1.27, name='flange left', id='bottom')
flange_right = geometry_object.Rect(
    50, h, 36.865, 1.27, name='flange right', id='bottom')
floor = geometry_object.Rect(
    13.135, 1.27, 73.73, 1.27, name='floor', id='bottom')

section_base = geometry_collection.GeometryCollection(
    (top, vertical_left, vertical_right, flange_left, flange_right, floor), (('bottom',),), name='section')

# section_base.display_geometry()


def make_extendo(n):
    extendo_h = 1.27*n

    top = geometry_object.Rect(0, h+x, 100, x, name='top', id='top', special_id='no top')
    vertical_left = geometry_object.Rect(
        11.865, h-extendo_h, 1.27, h-extendo_h, name='vertical left', id='bottom')
    vertical_right = geometry_object.Rect(
        86.865, h-extendo_h, 1.27, h-extendo_h, name='vertical right', id='bottom')
    flange_left = geometry_object.Rect(
        11.865+0.1, h, 1, 0.5, name='!exclude', id='bottom')
    flange_right = geometry_object.Rect(
        87.135-0.1, h, 1, 0.5, name='!exclude', id='bottom')
    # centering = geometry_object.Rect(18.135, h, 63.73, 1.27, name='center', id='bottom')
    extendo = geometry_object.Rect(
        11.865, h+x, 76.27, extendo_h+x, name='extendo', id='top')
    floor = geometry_object.Rect(
        13.135, 1.27, 73.73, 1.27, name='floor', id='bottom')

    return geometry_collection.GeometryCollection(
        (top, vertical_left, vertical_right, floor, extendo, flange_left, flange_right), (('bottom',), ('top',)), name=f'extendo_section-{n}')

# extendo_section.display_geometry()


top = geometry_object.Rect(0, h+x, 100, x, name='top')
bottom = geometry_object.Rect(
    11.865, h, 76.27, h, name='vertical left', id='bottom')

diaphragm = geometry_collection.GeometryCollection(
    (top, bottom), name='diaphragm', ignore_thin_plate=True)

# diaphragm.display_geometry()


def bounds_creator(intervals):
    types = ['section']
    bounds = [(0, intervals[0]-0.635)]
    sections = [section_base]

    for i in intervals[1:]:
        sections.append(diaphragm)
        sections.append(section_base)
        types.append('diaphragm')
        types.append('section')
        bounds.append([bounds[-1][1], bounds[-1][1]+1.27])
        bounds.append([bounds[-2][1]+1.27, i-0.635])

    types.append('section')
    sections.append(section_base)
    bounds.append([bounds[-1][1], 635])
    # bounds.pop(0)

    types.extend(types[::-1])
    sections.extend(sections[::-1])
    reverse_bound = []
    for bound in bounds[::-1]:
        reverse_bound.append([1270-bound[1], 1270-bound[0]])
    # bounds.extend(bounds[0:-1:-1])
    bounds.extend(reverse_bound)
    # print(bounds)
    # print(len(bounds))
    # print(types)
    # print(len(types))
    # print(sections)
    # print(len(sections))
    return bounds, types, sections


bounds, types, sections = bounds_creator([30, 80, 150, 220, 290, 370, 450, 550])

# for i, section in enumerate(sections):
#     if section.name == 'section':
#         sections[i] = extendo_section


print(len(bounds)) # 32

# sections[14]
sections[10] = make_extendo(2)
sections[12] = make_extendo(2)
sections[14] = make_extendo(2)
sections[15] = make_extendo(2)
sections[16] = make_extendo(2)
sections[17] = make_extendo(2)
sections[19] = make_extendo(2)
sections[21] = make_extendo(2)
# sections[15]
print(sections[14].top_flange)
# sections[14].display_geometry()

# print(bounds)
for i, section in enumerate(sections):
    print(section.name, types[i], bounds[i], i)
# print(types)

# types = ('section', 'diaphragm', 'section', 'diaphragm', 'section')

# cross_sections = bridge.CrossSections(
#     (section_base, diaphragm, section_base, diaphragm, section_base),
#     ((0, 399.365), (399.365, 400.635), (400.635, 799.365),
#      (799.365, 800.635), (800.635, 1200)),
#     types
# )

cross_sections = bridge.CrossSections(sections, bounds, types)

b = bridge.Bridge(1270, cross_sections)

print(b.get_board_amount()/10**6)

solve_maximum_forces(b, 400, 10)
display_graphs((graph_max_flexural, graph_max_shear, graph_max_thin_plate_buckling,
               graph_max_thin_plate_shear), 2, 2, 4, b, 400, 1)

# 549.8757728864432
