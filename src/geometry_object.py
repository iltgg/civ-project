class Rect():
    def __init__(self, x: float, y: float, x_length: float, y_length: float, tags=None, id=None) -> None:
        """create a geometry object, up is positive and right is positive

        Args:
            x (number): top left corner
            y (number): top left corner
            x_length (number): x length, right direction
            y_length (number): y length, down direction
            tags (str, optional): set a tag for use, format space separated 'ARG1 ARG2'. Defaults to None.
            id (str, optional): set an id for use. Defaults to None.
        """
        self.x = x
        self.y = y
        self.x_length = x_length
        self.y_length = y_length
        self.area = x_length*y_length
        self.tags = TagHandler(tags, 'display:True joint-display:True')

        self.id = id

        self.joints = None

    def find_area_below(self, y: float) -> float:
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

    def get_tag(self, tag) -> tuple:
        return self.tags.get_tag(tag)


class TagHandler():
    def __init__(self, tags, defaults) -> None:
        self.input_tags = tags
        self.tags = {}

        self.__init_tags(defaults)
        if tags:
            self.__init_tags(tags)
            

    def get_tag(self, tag):
        try:
            return self.tags[tag]
        except KeyError:
            return None

    def __init_tags(self, tags):
        for tag in tags.split(' '):
            args = tag.split(':')
            if args[1] == 'True':
                self.tags[args[0]] = True
            elif args[1] == 'False':
                self.tags[args[0]] = False
            elif args[1].isnumeric():
                self.tags[args[0]] = int(args[1])
            else:
                self.tags[args[0]] = args[1]
