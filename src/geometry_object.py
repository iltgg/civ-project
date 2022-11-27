class Rect():
    def __init__(self, x: float, y: float, x_length: float, y_length: float, tags=None, id=None, name=None, join_id=None, special_id=None) -> None:
        """create a geometry object, up is positive and right is positive

        Args:
            x (number): top left corner
            y (number): top left corner
            x_length (number): x length, right direction
            y_length (number): y length, down direction
            tags (str, optional): set a tag for use, format 'ARG1:VALUE1 ARG2:VALUE2 ...'. Defaults to None.
            id (str, optional): set an id for use, does not need to be unique. Defaults to None.
            join_id (str, optional): special join id, will attach all to all other geometry objects with same join id when a geometry collection is initialized. Only works if all geometry objects are collinear and vertically stacked Joints will be preserved for analysis and display, however the "joined" geometry objects will act as one rect (they are replaced by a new rect with combined dimensions). Defaults to None.
        """
        self.x = x
        self.y = y
        self.x_length = x_length
        self.y_length = y_length
        self.area = x_length*y_length
        self.tags = TagHandler(tags, 'display:True joint-display:True')

        self.id = id
        self.name = name
        self.join_id = join_id
        self.special_id = special_id

        self.horizontal = False
        self.vertical = False
        self.__find_horizontal_or_vertical()

        self.joints = None
        self.folds = None
        self.joined = None

    def find_area_below(self, y: float) -> float:  # might have bugs
        """find the area below a given y

        Args:
            y (number): height to find below

        Returns:
            number: area below y
        """
        if y > self.y-self.y_length and y < self.y:  # if between rectangle
            return self.x_length*(self.y_length - (self.y-y))
        if y >= self.y:  # if above rectangle
            return self.area
        if y <= self.y-self.y_length:  # if below rectangle
            return 0

    def find_centroid_below(self, y: float) -> float:  # might have bugs
        """find the centroid of the object below a given y

        Args:
            y (float): y

        Returns:
            float | None: height of centroid if it exists below
        """
        if y > self.y-self.y_length and y < self.y:  # if between rectangle
            new_y = y
            new_length = self.y_length - (self.y-new_y)
            # print(new_y, new_length)
            return (new_length/2)+new_y-new_length
        if y >= self.y:  # if above rectangle
            return self.find_centroid()
        if y <= self.y-self.y_length:  # if below rectangle
            return None

    def find_area_above(self, y: float) -> float:
        """find the area above a given y

        Args:
            y (float): height to find above

        Returns:
            number: area above y
        """
        if y > self.y-self.y_length and y < self.y:  # if between rectangle
            return self.x_length*(self.y-y)
        if y >= self.y:  # if above rectangle
            return 0
        if y <= self.y-self.y_length:  # if below rectangle
            return self.area

    def find_centroid_above(self, y) -> float:
        """find the centroid of the object above a given y

        Args:
            y (float): y

        Returns:
            float | None: height of centroid if it exists above
        """
        if y > self.y-self.y_length and y < self.y:  # if between rectangle
            new_length = self.y-y
            # print(new_y, new_length)
            return y-new_length+(new_length/2)
        if y >= self.y:  # if above rectangle
            return None
        if y <= self.y-self.y_length:  # if below rectangle
            return self.find_centroid()

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

    def __find_horizontal_or_vertical(self):
        """find and set if the rect is horizontal or vertical
        """
        if self.x_length > self.y_length:
            self.horizontal = True
        elif self.x_length < self.y_length:
            self.vertical = True

        # its a square if both this conditions pass


class TagHandler():
    def __init__(self, tags: str, defaults: str) -> None:
        """create a tag handler object, booleans and ints have their value casted

        tags must be in the format 'ARG1:VALUE1 ARG2:VALUE2 ...'

        Args:
            tags (str): tags
            defaults (str): default tags
        """
        self.input_tags = tags
        self.tags = {}

        self.__init_tags(defaults)
        if tags:
            self.__init_tags(tags)

    def get_tag(self, tag: str):
        """get the value of a tag, return None if nonexistent

        Args:
            tag (str): tag

        Returns:
            str | int | bool | None: the value of the tag if it exists
        """
        try:
            return self.tags[tag]
        except KeyError:
            return None

    def get_tags_str(self):
        return self.input_tags

    def __init_tags(self, tags: str) -> None:
        """sets tags

        Args:
            tags (str): tags to set
        """
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
