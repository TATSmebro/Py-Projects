from sp2_mandala import *

if __name__ == '__main__':
    m = Mandala(size = (600, 600), bgcolor = (0, 0, 0))

    for i in range(9):
        center1 = m.rotate_point((300,150), (300,300), i*40)
        center2 = m.rotate_point((300,200), (300,300), i*40)
        center3 = m.rotate_point((300,100), (300,300), i*40+20)

        rotation = i*40
        color1 = (i*15, 0, 128)
        color2 = (i*4, 139, 100-(i*4))
        color3 = (200, 165, i*20)
        
        m.draw_diamond(center1, 70, rotation, color1)
        m.draw_triangle(center2, 50, 180+rotation, color2)
        m.draw_fan(center3, 50, rotation+20, color3)

    m.show()
    m.save('sp2_output.png')