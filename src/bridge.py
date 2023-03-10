from typing import Iterable


class Bridge:
    def __init__(self, length: int, cross_sections: object) -> None:
        """Initialize a bridge object

        Args:
            length (number): length of the bridge in millimeters
            cross_sections (object): a cross sections object containing bridge cross sections
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

    def get_flexural_stress(self, x: float, y: float) -> float:
        """get the stress due to flexing at a given x and y

        Args:
            x (float): distance from left of bridge
            y (float): distance from bottom of bridge

        Returns:
            float: stress
        """
        section = self.cross_sections.get_cross_section(x)

        # (M*d)(I)

        M = self.get_bending_moment(x)
        I = section.I
        d = section.centroid - y

        return (M*d)/I

    def get_shear_stress(self, x: float, y: float, b=None) -> float:
        """get the stress due to shear at a given x and y

        Args:
            x (float): distance from left of bridge
            y (float): distance from bottom of bridge
            b (float, optional): width. if not given is calculated from cross section

        Returns:
            float: stress
        """
        section = self.cross_sections.get_cross_section(x)

        V = self.get_shear_force(x)
        Q = section.find_Q(y)
        I = section.I
        if not b:
            b = section.find_width(y)

        return (V*Q)/(I*b)

    def get_max_force_flexural(self, x: float, y: float, ignore_diaphragms=True) -> float:
        """get the max load the bridge can hold at a given x and y for flexural stress

        Args:
            x (float): distance from the left of bridge
            y (float): distance from bottom of bridge
            ignore_diaphragms (bool, optional): ignore diaphragms. Defaults to True.

        Returns:
            float: max load
        """

        if self.cross_sections.get_cross_section_type(x) == 'diaphragm':
            return None

        flexural_stress = self.get_flexural_stress(x, y)

        if flexural_stress > 0:
            return 30/flexural_stress * self.get_bending_moment(x)
        return -6/flexural_stress * self.get_bending_moment(x)

    def get_max_force_shear(self, x: float, y: float, b=None, shear_strength=4, ignore_diaphragms=True) -> float:
        """get the max load the bridge can hold at a given x and y for shear stress

        Args:
            x (float): distance from the left of bridge
            y (float): distance from bottom of bridge
            b (float, optional): width, if not given is calculated from cross section.
            shear_strength (int, optional): max shear stress. Defaults to 4.
            ignore_diaphragms (bool, optional): ignore diaphragms. Defaults to True.
        Returns:
            float: max load
        """
        if self.cross_sections.get_cross_section_type(x) == 'diaphragm':
            return None

        shear_stress = self.get_shear_stress(x, y, b)

        return shear_strength/shear_stress * self.get_shear_force(x)

    def get_unique_joints(self, ignore_diaphragms=True) -> list:
        """return a list of unique joints in the bridge

        Args:
            ignore_diaphragms (bool, optional): ignore diaphragms. Defaults to True.

        Returns:
            list: unique joints
        """
        joints = []

        for cross_section in self.cross_sections.unique_non_diaphragm_cross_sections:
            section_joints = cross_section.get_joint_heights()
            for joint in section_joints:
                joints.append(
                    (joint[0][0][1], cross_section.get_joint_width(joint), self.cross_sections.get_cross_section_bounds(cross_section), cross_section.name))

        return joints

    def get_max_force_tpb_top_flange(self, x: float, ignore_diaphragms=True) -> float:
        """return the max load the bridge can hold at a given x for thin plate buckling k = 4

        Args:
            x (float): distance from the left of bridge
            ignore_diaphragms (bool, optional): ignore diaphragms. Defaults to True.

        Returns:
            float: max load
        """

        if self.cross_sections.get_cross_section_type(x) == 'diaphragm':
            return None

        cross_section = self.cross_sections.get_cross_section(x)
        flanges = cross_section.top_flange

        maxes = []

        for flange in flanges:
            flexural_stress = self.get_flexural_stress(x, flange[2])
            maxes.append(-flange[-1]/flexural_stress)

        return min(maxes) * self.get_bending_moment(x)

    def get_max_force_tpb_side_flange(self, x, ignore_diaphragms=True):
        """return the max load the bridge can hold at a given x for thin plate buckling k = 0.425

        Args:
            x (float): distance from the left of bridge
            ignore_diaphragms (bool, optional): ignore diaphragms. Defaults to True.

        Returns:
            float: max load
        """
        if self.cross_sections.get_cross_section_type(x) == 'diaphragm':
            return None

        cross_section = self.cross_sections.get_cross_section(x)
        flanges = cross_section.side_flange

        maxes = []

        for flange in flanges:
            flexural_stress = self.get_flexural_stress(x, flange[2])
            maxes.append(-flange[-1]/flexural_stress)

        return min(maxes) * self.get_bending_moment(x)

    def get_max_force_tpb_vertical_flange(self, x, ignore_diaphragms=True):
        """return the max load the bridge can hold at a given x for thin plate buckling k = 6

        Args:
            x (float): distance from the left of bridge
            ignore_diaphragms (bool, optional): ignore diaphragms. Defaults to True.

        Returns:
            float: max load
        """
        if self.cross_sections.get_cross_section_type(x) == 'diaphragm':
            return None

        cross_section = self.cross_sections.get_cross_section(x)
        flanges = cross_section.vertical_flange

        maxes = []

        for flange in flanges:
            flexural_stress = self.get_flexural_stress(x, flange[2])
            maxes.append(-flange[-1]/flexural_stress)

        return min(maxes) * self.get_bending_moment(x)

    def get_max_force_tps(self, x, ignore_diaphragms=True):
        """return the max load the bridge can hold at a given x for thin plate shear buckling k = 5

        Args:
            x (float): distance from the left of bridge
            ignore_diaphragms (bool, optional): ignore diaphragms. Defaults to True.

        Returns:
            float: max load
        """
        if self.cross_sections.get_cross_section_type(x) == 'diaphragm':
            return None

        i = self.cross_sections.get_cross_section_index(x)
        bound = self.cross_sections.bounds[i]
        a = bound[1]-bound[0]+0.635

        cross_section = self.cross_sections.get_cross_section(x)
        flanges = cross_section.side_shear

        maxes = []

        for flange in flanges:
            shear_stress = self.get_shear_stress(x, cross_section.centroid)
            maxes.append(
                abs(cross_section.find_shear_plate_capacities(flange, a)/shear_stress))

        return abs(min(maxes)*self.get_shear_force(x))


class CrossSections:
    def __init__(self, cross_sections: Iterable, bounds: Iterable, types: Iterable) -> None:
        """create a cross sections object

        Args:
            cross_sections (Iterable): list of cross section
            bounds (Iterable): list of bounds for each cross section
            types (Iterable): list of types for each cross section (diaphragm, ...)
        """
        self.cross_sections = cross_sections
        self.bounds = bounds  # must be in order and correspond
        self.types = types
        self.unique_cross_sections = self.__return_unique_cross_sections(
            cross_sections)
        self.unique_non_diaphragm_cross_sections = self.__return_unique_cross_sections(
            cross_sections, 'diaphragm')

    def get_cross_section(self, x: float) -> object:
        """get the cross section at a given x

        Args:
            x (number): distance from left of bridge

        Returns:
            GeometryCollection: a geometry collection of the cross section
        """
        return self.cross_sections[self.__return_index(x)]

    def get_cross_section_index(self, x: float) -> int:
        """get the cross section index at a given x

        Args:
            x (number): distance from left of bridge

        Returns:
            int: the index of the cross section
        """
        return self.__return_index(x)

    def get_cross_section_type(self, x: float) -> str:
        """get the cross section type at a given x

        Args:
            x (number): distance from left of bridge

        Returns:
            str: the cross section type at x
        """
        return self.types[self.__return_index(x)]

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.cross_sections):
            self.n += 1
            return self.cross_sections[self.n-1], self.bounds[self.n-1], self.types[self.n-1]
        else:
            raise StopIteration

    def get_cross_section_bounds(self, cross_section: object) -> tuple:
        bounds = []

        for i, section in enumerate(self.cross_sections):
            if cross_section is section:
                bounds.append(self.bounds[i])

        return bounds

    def __return_index(self, x: float) -> int:
        """returns what index the x value falls within

        Args:
            x (number): an x value

        Returns:
            number: the index
        """
        i = 0
        while not self.__return_bounded(x, self.bounds[i]):
            i += 1

        return i

    def __return_bounded(self, x: float, bound: Iterable) -> bool:
        """return if the x is within a bound

        Args:
            x (number): an x value
            bound (Iterable): a bound in the from (a, b)

        Returns:
            bool: True if x is within the bound
        """
        # print(x)
        if x >= bound[0] and x <= bound[1]:
            return True
        else:
            return False

    def __return_unique_cross_sections(self, cross_sections: object, exclude=None) -> list:
        """return all unique cross sections in a bridge

        Args:
            cross_sections (object): a cross sections object
            exclude (_type_, optional): cross section types to exclude. Defaults to None.

        Returns:
            list: list of unique cross section objects
        """
        temp = []
        for i, cross_section in enumerate(cross_sections):
            if cross_section not in temp and self.types[i] != exclude:
                temp.append(cross_section)

        return temp
