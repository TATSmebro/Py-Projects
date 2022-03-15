from PIL import Image, ImageDraw
from math import sin, cos, pi

#center: int(x, y), side-length: float(x, y), rotation: (degrees), color: tuple(x, y, z)
def rotate_point(point, pivot, angle):
    adjusted_coord = (point[0]-pivot[0], point[1]-pivot[1])
    x = cos(pi*angle/180) * adjusted_coord[0] - sin(pi*angle/180) * adjusted_coord[1] + pivot[0]
    y = sin(pi*angle/180) * adjusted_coord[0] + cos(pi*angle/180) * adjusted_coord[1] + pivot[1]

    return x, y

#center: int(x, y), side-length: float(x, y), rotation: (degrees), color: tuple(x, y, z)
def draw_triangle(center, side_length, rotation, color):
    cent2vert = side_length/(3**0.5)
    
    pointA = rotate_point((center[0], center[1]-cent2vert), center, rotation)
    pointB = rotate_point(pointA, center, 120.0)
    pointC = rotate_point(pointA, center, -120.0)
    
    draw.line([pointA, pointB], fill = color, width = 1)
    draw.line([pointB, pointC], fill = color, width = 1)
    draw.line([pointC, pointA], fill = color, width = 1)

def draw_diamond(pivot, size, rotation, color):
    pointA = rotate_point((pivot[0], pivot[1] - size), pivot, rotation)
    pointB = rotate_point(pointA, pivot, 90.0)
    pointC = rotate_point((pivot[0], pivot[1] + 2*size), pivot, rotation)
    pointD = rotate_point(pointA, pivot, -90.0)

    draw.line([pointA, pointB], fill = color, width = 1)
    draw.line([pointB, pointC], fill = color, width = 1)
    draw.line([pointC, pointD], fill = color, width = 1)
    draw.line([pointD, pointA], fill = color, width = 1)

def draw_fan(pivot, size, rotation, color):
    bounding_box = [(pivot[0]-size, pivot[1]-size), (pivot[0]+size, pivot[1]+size)]
    pointA = rotate_point((pivot[0] + size, pivot[1]), pivot, rotation)
    pointB = rotate_point((pivot[0], pivot[1] + size), pivot, rotation)
    pointC = rotate_point((pivot[0] - size, pivot[1]), pivot, rotation)
    
    draw.arc(bounding_box, 180.0 + rotation, 0.0 + rotation, fill = color, width = 1)
    draw.line([pointA, pointB], fill = color, width = 1)
    draw.line([pointB, pointC], fill = color, width = 1)

def draw_circle(center, size, color):
    bounding_box = [(center[0]-size, center[1]-size), (center[0]+size, center[1]+size)]

    draw.arc(bounding_box, 0.0, 360.0, fill = color, width = 1)

canvas = Image.new("RGB", (200,200), (255,255,255))
draw = ImageDraw.Draw(canvas)

draw.point([(100,100), (100,100)], fill = (0, 0, 0))
draw_fan((100, 100), 30, 0, (255, 0, 0))

canvas.save("sample.png")