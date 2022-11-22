from typing import Iterable


class Bridge:
    def __init__(self, length: int, cross_sections: object) -> None:
        """Initialize a bridge object

        Args:
            length (number): length of the bridge (minus supports) in millimeters

        """
        self.length = length
        self.cross_sections = cross_sections

    def calculate_reaction_forces(self, load_positions: Iterable, loads: Iterable) -> tuple:
        """Calculates the reaction forces provided by A---------B\n
        Assumptions:
        - All point loads are downwards
        - Ignores self weight


        Args:
            load_positions (iterable): positions of point loads (mm)
            loads (iterable): force of each point load, index should match load_positions

        Returns:
            tuple: (A, B)
        """
        A = 0
        B = 0

        # Sum of moments around A
        M = 0
        for i, pos in enumerate(load_positions):
            M += loads[i]*pos

        # Sum of forces
        B = M/self.length
        A = sum(loads) - B

        return A, B

    def calculate_shear_force(self, load_positions: Iterable, loads: Iterable, reactions=False):
        """# Depreciated

        Calculates the shear force in bridge

        Args:
            load_positions (iterable): positions of point loads (mm)
            loads (iterable): force of each point load, index should match load_positions
            reactions (bool, optional): calculated using given values if not provided

        Returns:
            tuple: (positions (mm), shear force at position (N))
        """
        if not reactions:
            reactions = self.calculate_reaction_forces(load_positions, loads)

        x = []
        v = []

        x.append(0)
        v.append(0)

        x.append(0)
        v.append(reactions[0])

        for i, pos in enumerate(load_positions):
            x.append(pos)
            v.append(v[-1]-loads[i])

        x.append(self.length)
        v.append(v[-1]+reactions[1])

        return x, v

    def calculate_bending_moment(self, load_positions, loads, reactions=False):
        """# Depreciated

        Calculates bending moments in bridge

        Args:
            load_positions (iterable): positions of point loads (mm)
            loads (iterable): force of each point load, index should match load_positions
            reactions (bool, optional): calculated using given values if not provided

        Returns:
            tuple: (positions (N), bending moment at position (Nmm))
        """
        if not reactions:
            reactions = self.calculate_reaction_forces(load_positions, loads)

        x = []
        v = []

        x.append(0)
        v.append(reactions[0])

        for i, pos in enumerate(load_positions):
            x.append(pos)
            v.append(v[-1]-loads[i])

        x.append(self.length)

        widths = []
        for i in range(len(x)-1):
            widths.append(x[i+1]-x[i])

        m = []
        m.append(0)
        for i, shear in enumerate(v):
            m.append(m[-1]+shear*widths[i])

        return x, m

    def solve_shear_force(self, load_positions: Iterable, loads: Iterable, reactions=False):
        """solves and stores shear force in object, uses given loads and load positions 

        Args:
            load_positions (iterable): positions of point loads (mm)
            loads (iterable): force of each point load, index should match load_positions
            reactions (bool, optional): calculated using given values if not provided
        """

        if not reactions:
            reactions = self.calculate_reaction_forces(load_positions, loads)

        x = []
        v = []

        x.append(0)
        v.append(reactions[0])

        for i, pos in enumerate(load_positions):
            x.append(pos)
            v.append(v[-1]-loads[i])

        x.append(self.length)
        v.append(v[-1])

        self.x_v = x
        self.v = v

        self.load = sum(loads)

    def get_shear_force(self, x: float) -> float:
        """return the shear force at point x, requires valid shear force array in memory

        Args:
            x (number): position from the left of the bridge

        Returns:
            float: shear force
        """
        if x > self.x_v[-1]:
            return self.x_v[-1]

        if x == 0:
            return self.x_v[0]

        i = 0
        while not (x > self.x_v[i] and x <= self.x_v[i+1]):
            i += 1

        return self.v[i]

    def get_bending_moment(self, x: float) -> float:
        """return the bending moment at point x, requires valid shear force array in memory

        Args:
            x (number): position from the left of the bridge

        Returns:
            float: bending moment
        """
        area = 0

        i = 0
        while not (x > self.x_v[i] and x <= self.x_v[i+1]):
            i += 1

        for j in range(1, i+1):
            area += self.v[j-1]*(self.x_v[j]-self.x_v[j-1])

        area += self.get_shear_force(x)*(x-self.x_v[i])

        return area

    def get_flexural_stress(self, x, y):
        section = self.cross_sections.get_cross_section(x)

        # (M*d)(I)

        M = self.get_bending_moment(x)
        I = section.I
        d = section.centroid - y

        return (M*d)/I

    def get_max_force_flexural(self, x, y, ignore_diaphragms=True):
        if self.cross_sections.get_cross_section_type(x) == 'diaphragm':
            return None

        flexural_stress = self.get_flexural_stress(x, y)

        if flexural_stress > 0:
            return 30/flexural_stress * self.get_bending_moment(x)
        return -6/flexural_stress * self.get_bending_moment(x)


class CrossSections:
    def __init__(self, cross_sections: Iterable, bounds: Iterable, types: Iterable) -> None:
        self.cross_sections = cross_sections
        self.bounds = bounds  # must be in order and correspond
        self.types = types

    def get_cross_section(self, x):
        return self.cross_sections[self.__return_index(x)]

    def get_cross_section_type(self, x):
        return self.types[self.__return_index(x)]

    def __return_index(self, x):
        i = 0
        while not self.__return_bounded(x, self.bounds[i]):
            i += 1

        return i

    def __return_bounded(self, x, bound):
        if x >= bound[0] and x <= bound[1]:
            return True
        else:
            return False


if __name__ == "__main__":
    import train

    b = Bridge(1200, 0, 0)
    t = train.Train(100, 400)

    b.solve_shear_force(t.get_wheel_positions(), t.get_point_loads())
    # print(b.calculate_bending_moment(t.get_wheel_positions(),t.get_point_loads()))
    print(b.x_v)
    print(b.v)

    print(b.get_shear_force(600))
    print(b.get_bending_moment(600))
