class Bridge:
    def __init__(self, length) -> None:
        """Initialize a bridge object

        Args:
            length (number): length of the bridge (minus supports) in millimeters
        """
        self.length = length

    def calculate_reaction_forces(self, load_positions, loads) -> tuple:
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

    def calculate_shear_force(self, load_positions, loads, reactions=False):
        """Calculates the shear force in bridge

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
        """Calculates bending moments in bridge

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
