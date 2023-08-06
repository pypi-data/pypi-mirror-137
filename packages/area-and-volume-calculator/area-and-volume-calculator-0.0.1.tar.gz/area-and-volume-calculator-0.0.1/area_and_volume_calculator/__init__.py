# Area and Volume calculator by murtaza Chulawala
#defining classes to compute the areas of all the below given 2d and 3d figures with added volume computation for 3d figures
# Classes to compute Area of 2d figures
class Shape2d:
    class Circle:
        def Area_circle(radius):
            pi = 3.14159265359
            area = pi*radius**2
            return area

    class Square:
        def Area_square(side):
            area = side**2
            return area

    class Rectangle:
        def Area_rectangle(length, breadth):
            area = length * breadth
            return area

    class Triangle:
        def Area_triangle(base, height):
            area = (1/2) * base * height
            return area

    class Parallelogram:
        def Area_parallelogram(base, height):
            area = base * height
            return area

    class Trapezium:
        def Area_trapezium(apex_side, base, height):
            area = ((apex_side+base) * height)/2
            return area

    class Rhombus:
        def Area_rhombus(diagonal_1, diagonal_2):
            area = (diagonal_1*diagonal_2)/2
            return area

    class Hexagon:
        def Area_hexagon(side):
            area = ((3*(3**0.5))/2)*side**2
            return area

    class Pentagon:
        def Area_pentagon(side):
            area = (1/4)*((5*(5+(2*(5**0.5))))**0.5)*(side**2)
            return area

    class Ellipse:
        def Area_ellipse(minor_radius, major_radius):
            pi = 3.14159265359
            area = pi * minor_radius * major_radius
            return area

    class Octagon:
        def Area_octagon(side):
            area = 2*(1+(2**0.5))*side**2
            return area

#Classes to compute Area and Volume of 3d figures

class Shape3d:
    class Sphere:
        def Area_sphere(radius):
            pi = 3.14159265359
            area = 4 * pi * radius**2
            return area

        def Volume_sphere(radius):
            pi = 3.14159265359
            volume = (4/3) * pi * radius**3
            return volume

    class Cone:

        def Area_cone(radius, height):
            pi = 3.14159265359
            area = pi * radius * (radius + (height**2+radius**2)**0.5)
            return area

        def Volume_cone(radius, height):
            pi = 3.14159265359
            volume = pi * radius**2 * (height/3)
            return volume

    class Cylinder:
        def Area_cylinder(radius, height):
            pi = 3.14159265359
            area = (2*pi*radius*height)+(2*pi*radius**2)
            return area

        def Volume_cylinder(radius, height):
            pi = 3.14159265359
            volume = pi * (radius**2) * height
            return volume

    class Hemisphere:

        def Area_hemisphere(radius):
            pi = 3.14159265359
            area = 3 * pi * radius**2
            return area

        def Volume_hemisphere(radius):
            pi = 3.14159265359
            volume = (2/3) * pi * radius**3
            return volume

    class Cube:
        def Area_cube(side):
            area = 6 * (side**2)
            return area

        def Volume_cube(side):
            volume =side**3
            return volume

    class Cuboid:
        def Area_cuboid(length, breadth, height):
            area = 2 * ((length*height)+(breadth*height)+(length*breadth))
            return area

        def Volume_cuboid(length, breadth, height):
            volume = length * height * breadth
            return volume

    class Frustrum:

        def Area_frustrum(radius_1, radius_2, slant_height):
            pi = 3.14159265359
            area = 2*pi*((radius_1+radius_2)/2)*slant_height
            return area

        def Volume_frustrum(radius_1, radius_2, height):
            volume = ((3.14159265359 * height) * ((radius_1 ** 2)+(radius_1*radius_2) + (radius_2**2)))/3
            return volume

    class Regular_Tetrahedron:

        def Area_regular_tetrahedron(edge_length):
            area = (3**0.5)*edge_length**2
            return area

        def Volume_regular_tetrahedron(edge_length):
            area = (edge_length**3)/(6 * (2 **0.5))
            return area

    class Hexagonal_Pyramid:

        def Area_hexagonal_pyramid(base_edge ,height):
            area = (((3*(3**0.5))/2)*base_edge**2) + ((3 * base_edge) * (height**2 + ((3 * base_edge **2)/4))**0.5)
            return area

        def Volume_hexagonal_pyramid(base_edge ,height):
            volume = ((3 ** 0.5)/2) * (base_edge ** 2) * height
            return volume

    class Right_Regular_Hexagonal_Prism:

        def Area_right_regular_hexagonal_prism(base_edge ,height):
            area = 6 * base_edge * height + 3 * (3**0.5) * base_edge ** 2
            return area

        def Volume_right_regular_hexagonal_prism(base_edge ,height):
            volume = ((3 * (3 ** 0.5))/2) * (base_edge ** 2) * height
            return volume

    class Torus:

        def Area_torus(minor_radius, major_radius):
            pi = 3.14159265359
            area = (2 * pi * major_radius) * (2 * pi * minor_radius)
            return area

        def Volume_torus(minor_radius, major_radius):
            pi = 3.14159265359
            volume = (pi * (minor_radius ** 2)) * (2 * pi * major_radius)
            return volume

    class Octahedron:

        def Area_octahedron(base_edge):
            area = 2 * (3**0.5) * base_edge**2
            return area

        def Volume_octahedron(base_edge):
            volume = ((2**0.5)/3) * base_edge ** 3
            return volume

    class Right_Pentagonal_Pyramid:

        def Area_right_pentagonal_pyramid(base_edge, height):
            area = (5/4)*1.37638192047*(base_edge**2) + 5*(base_edge/2)*(((height**2)+((base_edge * 1.37638192047)/2)**2)**0.5)
            return area

        def Volume_right_pentagonal_pyramid(base_edge, height):
            volume = (5/12) * 1.37638192047 * height * (base_edge**2)
            return volume

    class Right_Regular_Pentagonal_Prism:

        def Area_right_regular_pentagonal_prism(base_edge, height):
            area = 5 * base_edge * height + 0.5 * ((5 * (5 + 2 * (5 ** 0.5))) ** 0.5) * base_edge ** 2
            return area

        def Volume_right_regular_pentagonal_prism(base_edge, height):
            volume = (1/4) * ((5*(5 + (2 * (5 ** 0.5))))**0.5) * (base_edge ** 2) * height
            return volume

    class Triangular_Prism:

        def Area_triangular_prism(base_edge_1, base_edge_2, base_edge_3, height, vertical_length, base):
            area = ((base_edge_1+base_edge_2+base_edge_3)*vertical_length) + (2*(0.5 * base * height))
            return area

        def Volume_triangular_prism(base_edge_1, base_edge_2, base_edge_3, height):
            volume = (1/4)*height*(((-base_edge_1**4) + 2 * ((base_edge_1 * base_edge_2)**2) + 2 * ((base_edge_1 * base_edge_3)**2) - (base_edge_2**4) + 2 * ((base_edge_2*base_edge_3)**2) - (base_edge_3 ** 4))**0.5)
            return volume

    class Right_Square_Pyramid:

        def Area_right_square_pyramid( base_edge, height):
            area = (base_edge ** 2) + (2 * base_edge) * ((((base_edge**2)/4) + height**2) ** 0.5)
            return area

        def Volume_right_square_pyramid(base_edge, height):
            volume = (base_edge ** 2) * (height/3)
            return volume

    class Dodecahedron:

        def Area_dodecahedron( edge):
            area = 3 * ((25 + 10 * (5 **0.5))**0.5) * edge ** 2
            return area

        def Volume_dodecahedron( edge):
            volume = ((15 + (7 * (5 ** 0.5)))/4) * edge ** 3
            return volume

    class Icosahedron:

        def Area_icosahedron( edge):
            area = 5 * (3 **0.5) * edge ** 2
            return area

        def Volume_icosahedron(edge):
            volume = ((5 * (3 +  (5 **0.5)))/12) * edge**3
            return volume

