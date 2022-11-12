class Train:
    def __init__(self, pos, weight) -> None:
        """Initialize a train object

        Args:
            pos (number): left-most position of the train in millimeters
            weight (number): weight of train in newtons
        """
        self.weight = weight
        self.pos = pos
        pass

    def get_wheel_positions(self) -> tuple:
        """Returns positions of wheels relative to left-most position of train

        Returns:
            tuple: tuple of wheel locations
        """
        return 52+self.pos, 228+self.pos, 392+self.pos, 568+self.pos, 732+self.pos, 908+self.pos

    def get_point_loads(self) -> tuple:
        """Returns a tuple of the load provided by each wheel

        Returns:
            tuple: tuple of loads, positive values
        """
        return (self.weight/6,)*6

    def get_point_load(self) -> float:
        """Returns the load given by a wheel

        Returns:
            float: load
        """
        return self.weight/6


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
        m = []

        # x.append(0)
        # v.append(0)
        x.append(0)
        v.append(reactions[0])

        for i, pos in enumerate(load_positions):
            x.append(pos)
            v.append(v[-1]-loads[i])

        x.append(self.length)
        # v.append(v[-1]+reactions[1])

        # print(x)
        # print(v)

        m.append(0)
        widths = []
        # widths.append(load_positions[0])
        # for i, pos in enumerate(load_positions):
        #     widths.append(pos-x[i])
        # widths.append(x[-1]-load_positions[-1])

        for i in range(len(x)-1):
            widths.append(x[i+1]-x[i])
        # print(widths)

        for i, shear in enumerate(v):
            m.append(m[-1]+shear*widths[i])     
        
        return x, m


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # t = Train(146, 400)
    t = Train(0, 400)
    b = Bridge(1200)

    # print(t.get_wheel_positions())
    # print(t.get_point_loads())
    # print(b.calculate_reaction_forces(t.get_wheel_positions(), t.get_point_loads()))

    shear_force_data = b.calculate_shear_force(
        t.get_wheel_positions(), t.get_point_loads())
    # print(shear_force_data[0])
    # print(shear_force_data[1])

    bending_moment_data = b.calculate_bending_moment(
        t.get_wheel_positions(), t.get_point_loads())
    # print(bending_moment_data[0])
    # print(bending_moment_data[1])
    
    # print()

    plt.subplot(211)
    plt.xlabel('distance (mm)')
    plt.ylabel('shear force (N)')
    plt.title('Shear Force Diagram')
    plt.step(shear_force_data[0], shear_force_data[1], where='post')

    plt.subplot(212)
    plt.xlabel('distance (mm)')
    plt.ylabel('bending moment (Nmm)')
    plt.title('Bending Moment Diagram')
    plt.gca().invert_yaxis()
    plt.plot(bending_moment_data[0], bending_moment_data[1])

    plt.tight_layout()
    plt.show()
