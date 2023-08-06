import pygame


class Rectangle:
    """
    This provides an abstraction of a rectangle shape.
    An instance is built from a pygame.Rect instance, the main difference being
    to support floating point coordinates.
    """

    def __init__(self, rectData: pygame.Rect):
        self.left = float(rectData.left)
        self.top = float(rectData.top)
        self.right = float(rectData.right)
        self.bottom = float(rectData.bottom)
        self.width = float(rectData.width)
        self.height = float(rectData.height)

    def position(self):
        """
        Returns the instance current position as a (x,y) tuple
        """
        return (self.left, self.top)

    def set_position(self, x, y):
        """
        Set the instance current position
        """
        self.left = x
        self.top = y
        self.right = self.left + self.width
        self.bottom = self.top + self.height

    def ltrb(self):
        """
        Returns a 4 items tuple for the left top right and bottom coordinates of the instance.
        """
        return (self.left, self.top, self.right, self.bottom)

    def xywh(self):
        """
        Returns a 4 items tuple for the left top coordinates and width and height of the instance.
        """
        return (self.left, self.top, self.width, self.height)

    def size(self):
        """
        Returns the instance width and height as a 2 items tuple.
        """
        return (int(self.width), int(self.height))

    def scale(self, factor):
        self.left *= factor
        self.top *= factor
        self.right *= factor
        self.bottom *= factor
        self.width *= factor
        self.height *= factor

    def copy_to_scale(self, factor):
        return Rectangle(pygame.Rect((
            self.left * factor,
            self.top * factor,
            self.width * factor,
            self.height * factor,
        )))
