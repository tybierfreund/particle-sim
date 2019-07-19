from graphics_class import Graphics, Rotations
from particle_class import FixedParticle, MovingParticle
from particle_module import instantiate_particles, draw_particles, find_maximums
import vector_math

# The processing library has builtin functions setup(), draw(), mousePressed(), and mouseDragged()
#
# setup() and draw() replace main(), with setup() being called at the beginning of the program
# and draw() being called continuously
#
# mousePressed() and mouseDragged() are event-based functions
#
# The global statements are necessary for these functions to share variables and objects
# between each other, as parameters cannot be passed into the functions
#
# Commander Schenk has approved the lack of a main() definition and the use of specific globals required by the library

def setup():
    global graphics, rotations, particles, max_size, max_radius, max_charge
    particles = instantiate_particles()

    # Main Frame
    size(800, 800, P3D)
    
    # Determines Length of Lines to Ensure Cube Shape
    if(width > height):
        graphics = Graphics(height, 8)
    else:
        graphics = Graphics(width, 8)
    rotations = Rotations()
    
    # Finds maximums to determine sizing and coloring
    for n in particles:
        particle_list = list(filter(lambda x: x != n, particles))
        n.do_motion(particle_list)
        
    max_size, max_radius, max_charge = find_maximums(particles)    


def draw():
    global graphics, rotations, particles, max_size, max_radius, max_charge
    background(0)
    stroke(200)
    strokeWeight(.25)
    lights()
    
    # Centers at Origin
    line_length = graphics.line_length
    translate((width/2)-(line_length/2), (height/2)-(line_length/2), -1.2*line_length)

    graphics.orient_grid(rotations.angleX, rotations.angleY)
    graphics.create_grid()
    
    draw_particles(particles, max_size, max_radius, max_charge, line_length)
    
    for n in particles:
        particle_list = list(filter(lambda x: x != n, particles))
        n.do_motion(particle_list)


def mousePressed():
    global rotations
    rotations.update_mouse_position(mouseX, mouseY)
    

def mouseDragged():
    global rotations
    rotations.update_angles(width, height, mouseX, mouseY)
