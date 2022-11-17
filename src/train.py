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