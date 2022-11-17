class Rect():
    def __init__(self, x: float, y: float, x_length: float, y_length: float) -> None:
        """create a geometry object, up is positive and right is positive

        Args:
            x (number): top left corner
            y (number): top left corner
            x_length (number): x length, right direction
            y_length (number): y length, down direction
        """
        self.x = x
        self.y = y
        self.x_length = x_length
        self.y_length = y_length
        self.area = x_length*y_length

    def find_area_below(self, y:float) -> float:
        """find the area below a given y

        Args:
            y (number): height to find below

        Returns:
            number: area below y
        """
        if y > self.y-self.y_length and y < self.y:  # if between rectangle
            return self.x_length*(y - self.y-self.y_length)
        if y > self.y:  # if above rectangle
            return self.area
        if y < self.y-self.y_length:  # if below rectangle
            return 0

    def find_I(self) -> float:
        """find the I_o for the rectangle, assumes the axis is a horizontal line

        Returns:
            number: I_o
        """
        return (self.x_length*self.y_length**3)/12

    def find_centroid(self) -> float:
        """find the centroid for the rectangle relative to y = 0, assumes the centroid is horizontal

        Returns:
            number: centroid relative to y = 0
        """
        # return (self.y+(self.y-self.y_length))/2
        return (self.y_length/2)+self.y-self.y_length

    def get_vertices(self) -> tuple:
        """get the coordinates of the vertices of the rectangle

        Returns:
            tuple: coordinates from top left corner, clockwise
        """
        return (self.x, self.y), (self.x+self.x_length, self.y), (self.x+self.x_length, self.y-self.y_length), (self.x, self.y-self.y_length)
