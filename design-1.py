from bridgeplotlib import *

# variables to play around with
x = 1.27  # top thickness
h = 100  # height of bridge

# make the base section
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


def make_extension(n: int) -> object:
    """create an base section with n extensions added to the top

    Args:
        n (number): the number of extensions to add

    Returns:
        object: a geometry collection object
    """
    extendo_h = 1.27*n

    top = geometry_object.Rect(
        0, h+x, 100, x, name='top', id='top', special_id='no top')
    vertical_left = geometry_object.Rect(
        11.865, h-extendo_h, 1.27, h-extendo_h, name='vertical left', id='bottom')
    vertical_right = geometry_object.Rect(
        86.865, h-extendo_h, 1.27, h-extendo_h, name='vertical right', id='bottom')
    flange_left = geometry_object.Rect(
        11.865+0.1, h, 1, 0.5, name='!exclude', id='bottom', tags='display:False')
    flange_right = geometry_object.Rect(
        87.135-0.1, h, 1, 0.5, name='!exclude', id='bottom', tags='display:False')
    extendo = geometry_object.Rect(
        11.865, h+x, 76.27, extendo_h+x, name='extendo', id='top')
    floor = geometry_object.Rect(
        13.135, 1.27, 73.73, 1.27, name='floor', id='bottom')

    return geometry_collection.GeometryCollection(
        (top, vertical_left, vertical_right, floor, extendo, flange_left, flange_right), (('bottom',), ('top',)), name=f'extended_section', joint_override=[((13.135, h), (86.865, h)), ((13.135, h-1.27), (86.865, h-1.27))])


# make the diaphragms
top = geometry_object.Rect(0, h+x, 100, x, name='top')
bottom = geometry_object.Rect(
    11.865, h, 76.27, h, name='vertical left', id='bottom')

diaphragm = geometry_collection.GeometryCollection(
    (top, bottom), name='diaphragm', ignore_thin_plate=True)


def bounds_creator(intervals: list):
    """return 3 arrays with valid bounds for a bridge with diaphragms occurring at the specified x values, mirrored over the center of the bridge

    Args:
        intervals (list): where to place diaphragms

    Returns:
        (list, list, list): bounds, types, geometry collections
    """
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

    types.extend(types[::-1])
    sections.extend(sections[::-1])
    reverse_bound = []
    for bound in bounds[::-1]:
        reverse_bound.append([1270-bound[1], 1270-bound[0]])
    bounds.extend(reverse_bound)
    return bounds, types, sections


# find the bounds
bounds, types, sections = bounds_creator(
    [30, 80, 150, 220, 290, 370, 450, 550])

# make an extension with n thickness
extension = make_extension(2)

# place extensions into proper section bounds
sections[4] = extension
sections[6] = extension
sections[8] = extension
sections[10] = extension
sections[12] = extension
sections[14] = extension
sections[15] = extension
sections[16] = extension
sections[17] = extension
sections[19] = extension
sections[21] = extension
sections[23] = extension
sections[25] = extension
sections[27] = extension

# section_base.display_geometry(bounding=(120, 120))
# diaphragm.display_geometry(bounding=(120, 120))
# extension.display_geometry(bounding=(120, 120))


cross_sections = bridge.CrossSections(sections, bounds, types)

b = bridge.Bridge(1270, cross_sections)

solve_maximum_forces(b, 400, 1)
display_graphs((graph_max_flexural, graph_max_shear, graph_max_thin_plate_buckling,
               graph_max_thin_plate_shear), 2, 2, 4, b, 400, 1)
