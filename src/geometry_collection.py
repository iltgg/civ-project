from typing import Iterable

from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt

from math import isclose

PRECISION = 0.001


class GeometryCollection:
    def __init__(self, geometry_objects: Iterable, geometry_object_groups=(), name=None) -> None:
        """create a geometry collection object, only supports Rect() geometry objects

        Args:
            geometry_objects (Iterable): an array of geometry_object
            geometry_object_groups (Iterable): (ID, ID, ...), (ID, ID, ...), ...
            name (str, optional): name of the collection
        """
        self.PRECISION = PRECISION
        self.geometry_objects = geometry_objects
        self.geometry_object_groups = geometry_object_groups
        self.name = name

        self.__find_joints()
        self.centroid = self.find_centroid()
        self.I = self.find_I()
        self.top = self.find_top()
        self.bottom = self.find_bottom()

    def find_centroid(self) -> float:
        """find the centroid for the collective relative to y = 0, assumes the centroid is horizontal

        Returns:
            number: centroid relative to y = 0
        """
        cen = 0
        sum_of_areas = 0
        for geometry_object in self.geometry_objects:
            cen += geometry_object.find_centroid()*geometry_object.area
            sum_of_areas += geometry_object.area

        return cen/sum_of_areas

    def find_I(self) -> float:
        """find the I for the collection, assumes the axis is a horizontal line

        Returns:
            number: I
        """
        I = 0
        cen = self.find_centroid()
        for geometry_object in self.geometry_objects:
            I += geometry_object.find_I()
            I += geometry_object.area * \
                (cen - geometry_object.find_centroid())**2

        return I

    def find_Q(self, y: float) -> float:
        """find the Q of the collection at a given y, assume the axis line is a horizontal line

        Args:
            y (float): _description_

        Returns:
            number: Q
        """
        Q = 0
        if y <= self.centroid:  # below centroid
            for geometry_object in self:
                # print(geometry_object.name)
                new_cen = geometry_object.find_centroid_below(y)
                # print(new_cen)
                if new_cen:
                    Q += geometry_object.find_area_below(y) * \
                        abs(self.centroid - new_cen)
        else:  # above centroid
            for geometry_object in self:
                # print(geometry_object.name)
                new_cen = geometry_object.find_centroid_above(y)
                # print(new_cen)
                if new_cen:
                    Q += geometry_object.find_area_above(y) * \
                        abs(self.centroid - new_cen)
        return Q

    def find_top(self) -> float:
        """find the top of the collection

        Returns:
            number: the y value of the top
        """
        top = self.centroid
        for geometry_object in self:
            if geometry_object.y > top:
                top = geometry_object.y
        return top

    def find_bottom(self) -> float:
        """find the bottom of the collection

        Returns:
            number: the y value of the bottom
        """
        bottom = self.centroid
        for geometry_object in self:
            if geometry_object.y-geometry_object.y_length < bottom:
                bottom = geometry_object.y-geometry_object.y_length
        return bottom

    def get_joint_width(self, joint_list: Iterable) -> float:
        b = 0
        for joint in joint_list:
            b += abs(joint[0][0] - joint[1][0])

        return b

    def get_joint_heights(self) -> list:
        """get an array with all the joints for each height

        Returns:
            list: a list with each index being a list of all joints at a height
        """
        joint_heights = []

        for geometry_object in self:
            for joint in geometry_object.joints:
                joint_heights.append(joint)

        sorted = [[]]
        for joint in joint_heights:
            for group in sorted:
                if len(group) == 0:
                    group.append(joint)
                else:
                    if self.__close(joint[0][1], group[0][0][1]):
                        same = False
                        for group_member in group:
                            if self.__check_same_joint(joint, group_member):
                                same = True

                        if not same:
                            group.append(joint)
                            continue
                    else:
                        sorted.append([joint])
                        continue

        return sorted

    def __check_same_joint(self, joint1: Iterable, joint2: Iterable) -> bool:
        """check if two joints are the same

        Args:
            joint1 (tuple): joint
            joint2 (tuple): other joint

        Returns:
            bool: True if matching
        """
        return self.__close(joint1[0][0], joint2[0][0]) and self.__close(joint1[1][0], joint2[1][0])

    def __close(self, x: float, y: float) -> bool:
        """wrapper for math.isclose with the PRECISION value

        Args:
            x (number): number to compare
            y (number): number to compare

        Returns:
            bool: True if isclose()
        """
        return isclose(x, y, abs_tol=self.PRECISION)

    def find_width(self, y: float) -> float:
        """finds the width of the collection at y, kinda hacky

        Args:
            y (number): height to find width at

        Returns:
            number: width
        """
        dy = 0.0001

        A1 = 0
        A2 = 0

        for geometry_object in self:
            A1 += geometry_object.find_area_below(y)
            A2 += geometry_object.find_area_below(y-dy)

        return (A1 - A2) / dy

    def __find_joints(self) -> None:
        """Find the joints of all geometry objects, automatically assigns the joints to each object
        """
        for i, geometry_object in enumerate(self.geometry_objects):
            vertices = geometry_object.get_vertices()
            joints = []
            folds = []

            for other_object in self.geometry_objects[:i]+self.geometry_objects[i+1:]:

                joint = self.__find_collinear_side(
                    vertices, other_object.get_vertices())
                same_group = False
                for group in self.geometry_object_groups:
                    if geometry_object.id in group and other_object.id in group:
                        same_group = True
                if joint:
                    if same_group:
                        folds.append(joint)
                    else:
                        joints.append(joint)

            geometry_object.joints = joints
            geometry_object.folds = folds

    def __find_collinear_side(self, vertices_1: Iterable, vertices_2: Iterable) -> tuple:
        """return the collinear side of two boxes, None if no collinear side exists

        Args:
            vertices_1 (iterable): vertices
            vertices_2 (iterable): vertices

        Returns:
            tuple: ((x1, y1), (x2, y2)), coordinates defining joint 
        """
        bounds = self.__get_bounds(vertices_1)
        collinear_side = []

        for vertex in vertices_2:
            for bound in bounds:
                bounded_x = vertex[0] < bound[0][0] and vertex[0] > bound[1][0]
                aligned_x = isclose(vertex[0], bound[0][0], abs_tol=self.PRECISION) or isclose(
                    vertex[0], bound[1][0], abs_tol=self.PRECISION)

                if bounded_x or aligned_x:
                    bounded_y = vertex[1] < bound[0][1] and vertex[1] > bound[1][1]
                    aligned_y = isclose(vertex[1], bound[0][1], abs_tol=self.PRECISION) or isclose(
                        vertex[1], bound[1][1], abs_tol=self.PRECISION)

                    if bounded_y or aligned_y:
                        collinear_side.append(vertex)

        collinear_side = list(set(collinear_side))  # hacky solution
        if len(collinear_side) == 2:
            return collinear_side

        bounds = self.__get_bounds(vertices_2)
        collinear_side = []

        for vertex in vertices_1:
            for bound in bounds:
                bounded_x = vertex[0] < bound[0][0] and vertex[0] > bound[1][0]
                aligned_x = isclose(vertex[0], bound[0][0], abs_tol=self.PRECISION) or isclose(
                    vertex[0], bound[1][0], abs_tol=self.PRECISION)

                if bounded_x or aligned_x:
                    bounded_y = vertex[1] < bound[0][1] and vertex[1] > bound[1][1]
                    aligned_y = isclose(vertex[1], bound[0][1], abs_tol=self.PRECISION) or isclose(
                        vertex[1], bound[1][1], abs_tol=self.PRECISION)

                    if bounded_y or aligned_y:
                        collinear_side.append(vertex)

        collinear_side = list(set(collinear_side))
        if len(collinear_side) == 2:
            return collinear_side

    def __get_bounds(self, vertices: Iterable) -> tuple:
        """generate the bounds of all sides of the box

        Args:
            vertices (iterable): vertices

        Returns:
            tuple: (((x1, y1), (x2, y2)), ((x2, y2), (x3, y3)), ...) clockwise tuple of box sides
        """
        bounds = []
        temp = vertices+(vertices[0],)

        for i, vertex in enumerate(vertices):
            bounds.append((vertex, temp[i+1]))

        # set order of coords so it is clockwise, consistency for comparison
        bounds[0] = bounds[0][1], bounds[0][0]
        bounds[3] = bounds[3][1], bounds[3][0]

        return bounds

    def find_thin_plate_type(self):
        pass

    def get_side_geometry(self):
        pass

    def display_geometry(self, bounding=(120, 100), window_size=(6, 6), show_joints=True, show_data=True) -> None:
        """display the geometry collection visually

        Args:
            bounding (list): (x, y) size to display
        """

        # https://matplotlib.org/stable/gallery/shapes_and_collections/compound_path.html#sphx-glr-gallery-shapes-and-collections-compound-path-py
        fig, ax = plt.subplots()

        codes = []
        vertices = []
        joint_codes = []
        joint_vertices = []
        fold_codes = []
        fold_vertices = []

        for geometry_object in self.geometry_objects:
            if geometry_object.get_tag('display'):
                codes += self.__return_code('square')
                vertices += self.__return_vertices(geometry_object)

                if show_joints:
                    if geometry_object.get_tag('joint-display'):
                        for joint in geometry_object.joints:
                            joint_codes += self.__return_code('line')
                            joint_vertices += joint
                            joint_vertices += (0, 0),

                        for fold in geometry_object.folds:
                            fold_codes += self.__return_code('line')
                            fold_vertices += fold
                            fold_vertices += (0, 0),

        path = Path(vertices, codes)
        pathpatch = PathPatch(path, facecolor='grey',
                              edgecolor='black', alpha=0.7)
        ax.add_patch(pathpatch)

        if show_joints:
            if len(joint_vertices) > 0:
                joint_path = Path(joint_vertices, joint_codes)
                joint_pathpatch = PathPatch(joint_path, edgecolor='red', lw=1)
                ax.add_patch(joint_pathpatch)
            if len(fold_vertices) > 0:
                fold_path = Path(fold_vertices, fold_codes)
                fold_pathpatch = PathPatch(fold_path, edgecolor='green', lw=1)
                ax.add_patch(fold_pathpatch)

        if show_data:
            ax.hlines(self.find_centroid(), 0,
                      bounding[0], color='blue', alpha=0.6, label='centroid')

            str = f'I: {self.find_I():.3f}\ncentroid: {self.find_centroid():.3f}'
            ax.text(bounding[0]-30, bounding[1]+1, str)

        ax.set_title('Cross section')
        ax.set_ylabel('y (mm)')
        ax.set_xlabel('x (mm)')
        fig.legend()
        fig.set_size_inches(window_size[0], window_size[1])
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlim(0, bounding[0])
        ax.set_ylim(0, bounding[1])
        ax.minorticks_on()
        ax.grid(which='both', linestyle='--', color='grey', alpha=0.5)

        plt.show()

    def __return_code(self, type: str) -> list:
        """return code for drawing path

        Args:
            type (str): type of path, (square, ...)

        Returns:
            list: code for pathing given type
        """
        if type == 'square':
            return [Path.MOVETO]+[Path.LINETO]*3+[Path.CLOSEPOLY]
        if type == 'line':
            return [Path.MOVETO]+[Path.LINETO]+[Path.CLOSEPOLY]

    def __return_vertices(self, geometry_object: object) -> list:
        """return the vertices for drawing of a geometry object

        Args:
            geometry_object (object): a geometry_object

        Returns:
            list: vertices + and extra (0, 0)
        """
        v = []
        for i in geometry_object.get_vertices():
            v.append(i)

        v.append((0, 0))

        return v

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.geometry_objects):
            self.n += 1
            return self.geometry_objects[self.n-1]
        else:
            raise StopIteration


if __name__ == "__main__":
    from geometry_object import *
    r1 = Rect(0, 75+1.27, 100, 1.27, name='top')  # top

    r2 = Rect(10, 75, 1.27, 75-1.27, id='folded-section',
              name='vertical-left')  # verticals
    r3 = Rect(90-1.27, 75, 1.27, 75-1.27,
              id='folded-section', name='vertical right')

    r4 = Rect(10+1.27, 75, 5, 1.27, id='folded-section',
              name='nib-left')  # lil nibs
    r5 = Rect(90-5-1.27, 75, 5, 1.27, id='folded-section', name='nib-right')

    r6 = Rect(10, 1.27, 80, 1.27, id='folded-section', name='bottom')  # bottom

    gc = GeometryCollection((r1, r2, r3, r4, r5, r6), (('folded-section',),))

    print(gc.get_joint_width(gc.get_joint_heights()[0]))

    # for obj in gc:
    #     print(obj.name, obj.joints)
    gc.display_geometry((120, 100), (6, 6), True)
