from typing import Iterable

from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt


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
            I += geometry_object.find_I()
            I += geometry_object.area * \
                (cen - geometry_object.find_centroid())**2

        return I

    def find_Q(self, y):
        pass

    def display_geometry(self, bounding) -> None:
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
        pathpatch = PathPatch(path, facecolor='grey', edgecolor='black', alpha=0.7)

        fig, ax = plt.subplots()

        ax.add_patch(pathpatch)
        ax.hlines(self.find_centroid(), 0, bounding[0], color='blue', alpha=0.6, label='centroid')

        ax.set_title('Cross section')
        ax.set_ylabel('y (mm)')
        ax.set_xlabel('x (mm)')
        fig.legend()
        fig.set_size_inches(8,8)
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


if __name__ == "__main__":
    from geometry_object import *
    r1 = Rect(0, 75+1.27, 100, 1.27)  # top

    r2 = Rect(10-1.27, 75, 1.27, 75-1.27)  # verticals
    r3 = Rect(90, 75, 1.27, 75-1.27)

    r4 = Rect(10, 75, 5, 1.27)  # lil nibs
    r5 = Rect(90-5, 75, 5, 1.27)

    r6 = Rect(10-1.27, 1.27, 80+1.27+1.27, 1.27)  # bottom

    gc = GeometryCollection((r1, r2, r3, r4, r5, r6))

    print(gc.find_centroid())
    print(gc.find_I())

    gc.display_geometry((120,100))
