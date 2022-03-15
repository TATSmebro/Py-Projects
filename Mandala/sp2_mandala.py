import PIL.Image, PIL.ImageDraw
from math import sin, cos, pi

class Mandala():

    def __init__(self, size, bgcolor):
        self.size = size
        self.bgcolor = bgcolor
        self.canvas = PIL.Image.new('RGB', size, bgcolor)
        self.draw = PIL.ImageDraw.Draw(self.canvas)

    def show(self):
        self.canvas.show()
        
    def save(self, filename):
        self.canvas.save(filename)

    #point: (x, y), pivot: (x, y), angle: (degrees)
    def rotate_point(self, point, pivot, angle):
        adjusted_coord = (point[0]-pivot[0], point[1]-pivot[1])
        x = cos(pi*angle/180) * adjusted_coord[0] - sin(pi*angle/180) * adjusted_coord[1] + pivot[0]
        y = sin(pi*angle/180) * adjusted_coord[0] + cos(pi*angle/180) * adjusted_coord[1] + pivot[1]

        return x, y
    
    #center: int(x, y), side-length: float(x, y), rotation: (degrees), color: tuple(x, y, z)
    def draw_triangle(self, center, side_length, rotation, color):
        cent2vert = side_length/(3**0.5)
        
        pointA = self.rotate_point((center[0], center[1]-cent2vert), center, rotation)
        pointB = self.rotate_point(pointA, center, 120.0)
        pointC = self.rotate_point(pointA, center, -120.0)
        
        self.draw.line([pointA, pointB], fill = color, width = 4)
        self.draw.line([pointB, pointC], fill = color, width = 4)
        self.draw.line([pointC, pointA], fill = color, width = 4)

    def draw_diamond(self, pivot, size, rotation, color):
        pointA = self.rotate_point((pivot[0], pivot[1]-size), pivot, rotation)
        pointB = self.rotate_point(pointA, pivot, 90.0)
        pointC = self.rotate_point((pivot[0], pivot[1] + 2*size), pivot, rotation)
        pointD = self.rotate_point(pointA, pivot, -90.0)

        self.draw.line([pointA, pointB], fill = color, width = 4)
        self.draw.line([pointB, pointC], fill = color, width = 4)
        self.draw.line([pointC, pointD], fill = color, width = 4)
        self.draw.line([pointD, pointA], fill = color, width = 4)

    def draw_fan(self, pivot, size, rotation, color):
        bounding_box = [(pivot[0]-size, pivot[1]-size), (pivot[0]+size, pivot[1]+size)]
        pointA = self.rotate_point((pivot[0] + size, pivot[1]), pivot, rotation)
        pointB = self.rotate_point((pivot[0], pivot[1] + size), pivot, rotation)
        pointC = self.rotate_point((pivot[0] - size, pivot[1]), pivot, rotation)
        
        self.draw.arc(bounding_box, 180.0 + rotation, 0.0 + rotation, fill = color, width = 4)
        self.draw.line([pointA, pointB], fill = color, width = 4)
        self.draw.line([pointB, pointC], fill = color, width = 4)