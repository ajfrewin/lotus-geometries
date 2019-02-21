import cairo
from math import *
import random

def regular_polygon(n, center, radius, rotation=0):
    '''

    :param n: number of sides
    :param center: coordinates of center of polygon
    :param radius: length from center to a perpendicular edge
    :param rotation: rotational offset
    :return: vertices of the regular polygon
    '''
    thta_interval = 360/n
    thta = -90 + rotation
    vertices = []
    if n%2!=0:
        for i in range(0,n):
            vertices.append([center[0]+radius*cos(radians(thta)), center[1]+radius*sin(radians(thta))])
            thta = thta+thta_interval
        return vertices
    else:
        thta = thta + thta_interval/2
        for i in range(0,n):
            vertices.append([center[0] + radius * cos(radians(thta)), center[1] + radius * sin(radians(thta))])
            thta = thta + thta_interval

        return vertices

def draw_shape(verts):
    '''
    draws a shape given its vertices
    :param verts: list containing x-y coordinate pairs of shape vertices
    :return: draws the shape
    '''
    ctx.move_to(verts[0][0], verts[0][1])
    for i in range(1,len(verts)):
        ctx.line_to(verts[i][0],verts[i][1])
    ctx.line_to(verts[0][0],verts[0][1])

def draw_polygon(n, center, r, color, rotation=0, fill=False):
    '''
    Draws regular polygon
    :param n: number of polygon sides
    :param center: center of the polygon
    :param r: radius
    :param color: color in RGB fraction format [R, G, B]
    :param fill: if you want to fill in the shape
    :return:
    '''
    verts = regular_polygon(n, center, r, rotation)
    ctx.set_source(cairo.SolidPattern(*color))
    draw_shape(verts)
    if fill:
        ctx.close_path()
        ctx.fill()
    ctx.stroke()

def lotus(center, leaves, length, color, scale=2, rotation=0, fill=False):
    '''
    Draws radially symetric lotus petals
    :param center: center of the petals
    :param leaves: number of petals
    :param length: length of each petal
    :param rotation: initial rotation offset
    :return: draws the lotus flower
    TO DO: make scaling factor for non-symetric petals
    '''
    verts = regular_polygon(leaves, center, length, rotation)
    thta_interval = 2*pi/leaves
    width = length/scale
    if leaves%2==0:
        thta = radians(-90) + thta_interval/2
    else:
        thta = radians(-90)
    thta = thta + radians(rotation)
    for vert in verts:

        x1 = center[0]
        y1 = center[1]

        x21 = center[0] + width * cos(thta) + length/2*sin(thta)
        y21 = center[1] + width*sin(thta) - length/2*cos(thta)

        x22 = center[0] + width * cos(thta) - length/2 * sin(thta)
        y22 = center[1] + width*sin(thta) + length/2*cos(thta)

        x3 = vert[0]
        y3 = vert[1]
        ctx.curve_to(x1, y1, x21, y21, x3, y3)
        ctx.curve_to(x3, y3, x22, y22, x1, y1)
        thta = thta+thta_interval

    ctx.set_source(cairo.SolidPattern(*color))
    if fill:
        ctx.close_path()
        ctx.fill()
    ctx.stroke()


sides = [2,3,4,5,6,7,8,9,10,11,12,13]
sides.reverse()
def off_box(sides):
    '''
    Creates 2 sets of telescoping polygons offset by half angles
    :param sides: number of sides of the polygon
    :return: drawing
    '''
    r = 250
    G = 0
    for n in sides:
        draw_polygon(4, [250,250], r, [0, G, 0])
        draw_polygon(4, [250,250], r, [G, 0, 0], rotation=360/4/2)
        r = r - 20
        G = G + .05

def spiral_poly(sides, layers, thta_interval=2):
    '''
    Sp[iraling polygon pattern
    :param sides: polygon sides
    :param layers: number of spiral layers
    :return: drawing
    '''
    r = 10 # set initial radius
    r_interval = 400/layers
    thta = 0 # set angle
    for i in range(layers):
        draw_polygon(sides,[250,250],r,[0,.5,0],rotation=thta)
        thta = thta + thta_interval # increase angle
        r = r + r_interval # increase radius

def sketch_lotus(n, rotation=0):
    '''
    Cool mandala effected where it appears sketched or caligraphied
    :param n: intensity of effect
    :return: drawing
    '''
    S = 2
    for i in range(n):
        lotus([250,250], 12, 250, [.5, 0, 0],rotation=rotation, scale=S)
        S = S+1 # increase scale factor

def blooming_lotus(center, leaves, layers, rstart, trace=True, cmap='r'):
    '''
    Basically a layered lotus efect
    :param center: [x,y] coordinates of the mandala center
    :param leaves: number of leaves on the mandala
    :param layers: number of layers in the bloom
    :param rstart: maximum radius
    :param trace: if True, traces each layer to give more defined image
    :param cmap: color map, 'r' for red, 'g' for green, 'b' or other for blue
    :return:
    '''

    r = rstart
    c_interval = .8/layers
    r_interval = int((rstart/layers))

    if cmap=='r':
        color=[.2,0,0]
        idx = 0
    elif cmap=='g':
        color=[0,.2,0]
        idx = 1
    else:
        color=[0,0,.2]
        idx = 2
    for i in range(layers):
        lotus(center, leaves, r, color, fill=True)
        if trace: lotus(center, leaves, r, [0,0,0])
        r = r - r_interval
        color[idx] = color[idx] + c_interval

def lotus_scatter(n):
    '''
    scatters a few lotuses randomly about the landscape
    :param n: number of lotuses to scatter
    :return: drawing
    '''
    for i in range(n):
        center = [random.randint(50,450),random.randint(50,450)]
        color = random.randint(0, 2)
        if color == 0:
            cmap = 'r'
        elif color == 1:
            cmap = 'g'
        else:
            cmap = 'b'
        rstart = min(center[0],center[1],450-center[0]+50, 450-center[1]+50)
        layers=int(rstart/10)
        blooming_lotus(center,12,layers,rstart,cmap=cmap)

def spiral_lotus(center, leaves, layers, rstart = 250, thta_interval=10, cmap='r'):
    '''

    :param leaves: number of lotus leaves
    :param layers: number of layers in the spiral
    :param thta_interval: angle interval between layers
    :return:
    '''
    if cmap=='r':
        color=[.5,0,0]
    elif cmap=='g':
        color=[0,.5,0]
    else:
        color=[0,0,.5]
    r = rstart  # set initial radius
    r_interval = (rstart-10) / layers
    thta = 0  # set angle
    for i in range(layers):
        lotus(center,leaves,r,color,scale=10,rotation=thta,fill=True)
        lotus(center, leaves, r, [0, 0, 0], scale=10, rotation=thta)
        thta = thta + thta_interval  # increase angle
        r = r - r_interval  # increase radius

def spiral_scatter(n):
    '''
    :param n: number of lotuses to spiral
    :return: drawing
    '''
    for i in range(n):
        center = [random.randint(50,450),random.randint(50,450)]
        color = random.randint(0, 2)
        if color == 0:
            cmap = 'r'
        elif color == 1:
            cmap = 'g'
        else:
            cmap = 'b'
        rstart = min(center[0],center[1],450-center[0]+50, 450-center[1]+50)
        layers=int(rstart/10)
        spiral_lotus(center,random.randint(3,10),layers,rstart,cmap=cmap)

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
ctx = cairo.Context(surface)



surface.write_to_png('spiral_poly.png')