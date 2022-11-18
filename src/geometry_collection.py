from typing import Iterable

from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt

from math import isclose


class GeometryCollection:
    def __init__(self, geometry_objects: Iterable) -> None:
        """create a geometry collection object

        Args:
            geometry_objects (Iterable): an array of geometry_object
        """
        self.geometry_objects = geometry_objects

    def find_centroid(self) -> float:
        """find the centroid for the collective relative to y = 0, assumes the centroid is horizontal

        Returns:
            number: centroid relative to y = 0
        """
        cen = 0
        sum_of_areas = 0
        for geometry_object in self.geometry_objects:
            cen += geometry_object.find_centroid()*geometry_object.area
            # print(geometry_object.find_centroid())
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
            # print(geometry_object.area)
            I += geometry_object.find_I()
            I += geometry_object.area * \
                (cen - geometry_object.find_centroid())**2

        return I

    def find_Q(self, y):
        pass

    def find_joints(self):
        for i, geometry_object in enumerate(self.geometry_objects):
            verts = geometry_object.get_vertices()
            intersectors = []

            print(i, verts)

            for other_object in self.geometry_objects[:i]+self.geometry_objects[i+1:]:
                touching = self.__find_collinear_side(
                    verts, other_object.get_vertices())

                if touching:
                    intersectors.append(touching)

            geometry_object.joints = intersectors

    # def __find_collinear_side(self, vertices_one: tuple, vertices_two: tuple) -> tuple | None:
    #     bounds = self.__get_bounds(vertices_one)
    #     collinear_side = []

    #     for vertex in vertices_two:
    #         for bound in bounds:
    #             # print(bound)
    #             # print(vertex)
    #             if (vertex[0] <= bound[0][0] or isclose(vertex[0], bound[0][0])) and (vertex[0] >= bound[1][0] or isclose(vertex[0], bound[0][1])):
    #                 if (vertex[1] <= bound[0][1] or isclose(vertex[1], bound[0][1])) and (vertex[1] >= bound[1][1] or isclose(vertex[1], bound[0][1])):
    #                     collinear_side.append(vertex)

    #     if len(collinear_side) == 2:
    #         return collinear_side

    #     return None
    def __find_collinear_side(self, vert1, vert2):
        bounds = self.__get_bounds(vert1)
        collinear_side = []

        for vertex in vert2:
            for bound in bounds:
                if vertex[0] <= bound[0][0] and vertex[0] >= bound[1][0]:
                    if vertex[1] <= bound[0][1] and vertex[1] >= bound[1][1]:
                        cl = self.__is_collinear(bound, vertex)
                        if cl:
                            collinear_side.append(vertex)

        if len(collinear_side) == 2:
            return collinear_side

    def __is_collinear(self, line, vert):
        return self.collinear(line[0], line[1], vert)

    def collinear(self, p0, p1, p2):
        x1, y1 = p1[0] - p0[0], p1[1] - p0[1]
        x2, y2 = p2[0] - p0[0], p2[1] - p0[1]
        return isclose(abs(x1 * y2 - x2 * y1), 0)

    def __get_bounds(self, vertices):
        bounds = []
        temp = vertices+(vertices[0],)
        # print(temp)
        # print(vertices)
        for i, vertex in enumerate(vertices):
            bounds.append((vertex, temp[i+1]))

        # clockwise
        bounds[0] = bounds[0][1], bounds[0][0]
        bounds[3] = bounds[3][1], bounds[3][0]

        return bounds

    def find_thin_plate_type(self):
        pass

    def display_geometry(self, bounding, window_size, show_joints=False) -> None:
        """display the geometry collection visually

        Args:
            bounding (list): (x, y) size to display
        """

        # https://matplotlib.org/stable/gallery/shapes_and_collections/compound_path.html#sphx-glr-gallery-shapes-and-collections-compound-path-py
        codes = []
        vertices = []
        for geometry_object in self.geometry_objects:
            codes += self.__return_code('square')
            vertices += self.__return_vertices(geometry_object)

        path = Path(vertices, codes)
        pathpatch = PathPatch(path, facecolor='grey',
                              edgecolor='black', alpha=0.7)

        fig, ax = plt.subplots()

        ax.add_patch(pathpatch)
        ax.hlines(self.find_centroid(), 0,
                  bounding[0], color='blue', alpha=0.6, label='centroid')

        joint_codes = []
        joint_vertices = []
        if show_joints:
            for geometry_object in self.geometry_objects:
                if geometry_object.joints:
                    for joint in geometry_object.joints:
                        joint_codes += self.__return_code('line')
                        joint_vertices += joint
                        joint_vertices += (0, 0),
                        # joint_vertices += joint[1]

            print(joint_vertices)
            print(joint_codes)
            joint_path = Path(joint_vertices, joint_codes)
            joint_pathpatch = PathPatch(joint_path, edgecolor='blue', lw=3)
            ax.add_patch(joint_pathpatch)

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
    r1 = Rect(0, 75+1.27, 100, 1.27)  # top

    r2 = Rect(10, 75, 1.27, 75-1.27)  # verticals
    r3 = Rect(90-1.27, 75, 1.27, 75-1.27)

    r4 = Rect(10+1.27, 75, 5, 1.27)  # lil nibs
    r5 = Rect(90-5-1.27, 75, 5, 1.27)

    r6 = Rect(10, 1.27, 80, 1.27)  # bottom

    gc = GeometryCollection((r1, r2, r3, r4, r5, r6))

    # print(gc.find_centroid())
    # print(gc.find_I())

    gc.find_joints()

    for i in gc:
        print(i.joints)
    # print(r1.joints)

    gc.display_geometry((120, 100), (6, 6), True)
