from javax.swing import JLabel, JOptionPane
from java.awt import Font
from particle_class import FixedParticle, MovingParticle
import vector_math


def input(prompt):
    """Creates new window that allows for user input"""
    label = JLabel(prompt, JLabel.CENTER)
    label.setFont(Font('Arial', Font.PLAIN, 35))
    return JOptionPane.showInputDialog(frame, label, '', JOptionPane.PLAIN_MESSAGE)


def print_message(message):
    """Creates new window that displays message"""
    label = JLabel(message, JLabel.CENTER)
    label.setFont(Font('Arial', Font.PLAIN, 35))
    JOptionPane.showMessageDialog(frame, label, '', JOptionPane.PLAIN_MESSAGE)
    

def print_error(error):
    """Creates new window that displays error message"""
    label = JLabel(error, JLabel.CENTER)
    label.setFont(Font('Arial', Font.PLAIN, 35))
    JOptionPane.showMessageDialog(frame, label, '', JOptionPane.ERROR_MESSAGE)


def check_input(prompt, *words, **bounds):
    """Checks that input is an int in bounds"""
    # Assigns bounds
    try:
        ubound = bounds['ubound']
    except KeyError:
        ubound = None
    try:
        lbound = bounds['lbound']
    except KeyError:
        lbound = None

    var = input(prompt)
    if(var == None):
            var = check_input(prompt, *words, lbound=lbound, ubound=ubound)
    try:
        var = int(var)
        if(ubound != None):
            if(var >= ubound):
                print_error('Must be less than' + ' ' + str(ubound))
                var = check_input(prompt, *words, lbound=lbound, ubound=ubound)
        if(lbound != None):
            if(var < lbound):
                print_error('Must be greater than or equal to' + ' ' + str(lbound))
                var = check_input(prompt, *words, lbound=lbound, ubound=ubound)
    except ValueError:
        if(var in words):
            return var
        else:
            print_error('Must be an integer')
            var = check_input(prompt, *words, lbound=lbound, ubound=ubound)
    finally:
        return var


def check_input_float(prompt, *words, **bounds):
    """Checks that input is a float in bounds"""
    # Assigns bounds
    try:
        ubound = bounds['ubound']
    except KeyError:
        ubound = None
    try:
        lbound = bounds['lbound']
    except KeyError:
        lbound = None

    var = input(prompt)
    if(var == None):
            var = check_input_float(prompt, *words, lbound=lbound, ubound=ubound)
    try:
        var = float(var)
        if(ubound != None):
            if(var >= ubound):
                print_error('Must be less than' + ' ' + str(ubound))
                var = check_input_float(prompt, *words, lbound=lbound, ubound=ubound)
        if(lbound != None):
            if(var <= lbound):
                print_error('Must be greater than' + ' ' + str(lbound))
                var = check_input_float(prompt, *words, lbound=lbound, ubound=ubound)
    except ValueError:
        if(var in words):
            return var
        else:
            print_error('Must be a float')
            var = check_input_float(prompt, *words, lbound=lbound, ubound=ubound)
    finally:
        return var


def instantiate_particles():
    """Instantiates particles using user input"""
    particles = []
    inputted_data, position, velocity, spin = [], [], [], []
    stop = False
    while(not stop):
        retry = True
        label = JLabel('Would You Like to Import from File', JLabel.CENTER)
        label.setFont(Font('Arial', Font.PLAIN, 35))
        file_use = JOptionPane.showConfirmDialog(frame, label, '', JOptionPane.YES_NO_OPTION)
        while(retry):
            if(file_use == 0):
                file_name = input('File Name:')
                if(file_name != None):
                    file = loadStrings(file_name)
                    if(not file):
                        print_error('Empty File')
                    else:
                        t_step = float(file[0])
                        line_pos = 2
                        while(line_pos < len(file)):
                            data = file[line_pos].split(' ')
                            data = list(map(lambda x: float(x), data))
                            
                            if(line_pos+1 < len(file)):
                                if(file[line_pos+1]):
                                    texture_data = file[line_pos+1]
                                    line_pos += 3
                                else:
                                    texture_data = None
                                    line_pos += 2
                            else:
                                texture_data = None
                                line_pos += 2
                                
                            if(len(data) > 9):
                                init_pos = data[3:6]
                                init_vel = data[6:9]
                                init_spin = data[9:12]
                                particles.append(MovingParticle(*data[:3], init_pos=init_pos, init_vel=init_vel, init_spin=init_spin, t_step=t_step, texture_data=texture_data))
                            else:
                                init_pos = data[3:6]
                                init_spin = data[6:9]
                                particles.append(FixedParticle(*data[:3], init_pos=init_pos, init_spin=init_spin, t_step=t_step, texture_data=texture_data))  
                        retry = False
                        stop = True 
                else:
                    retry = False        
            else:
                label = JLabel('Choose Particle Type:', JLabel.CENTER)
                label.setFont(Font('Arial', Font.PLAIN, 35))
                particle_type = JOptionPane.showInputDialog(frame, label, '', JOptionPane.PLAIN_MESSAGE, None, ['Fixed', 'Moving'], '')
                
                print_message('Type \'retry\' to retry and \'stop\' to stop')
                mass = check_input_float('Mass: ', 'retry', 'stop', lbound=0)
                inputted_data.append(mass)
                
                charge = check_input_float('Charge: ', 'retry', 'stop')
                inputted_data.append(charge)
                
                radius = check_input_float('Radius: ', 'retry', 'stop', lbound=0)
                inputted_data.append(radius)
                
                position.append(check_input_float('Initial X Position: ', 'retry', 'stop'))
                position.append(check_input_float('Initial Y Position: ', 'retry', 'stop'))
                position.append(check_input_float('Initial Z Position: ', 'retry', 'stop'))
                inputted_data.append(position)
                
                if(particle_type == 'Moving'):
                    velocity.append(check_input_float('Initial X Velocity: ', 'retry', 'stop'))
                    velocity.append(check_input_float('Initial Y Velocity: ', 'retry', 'stop'))
                    velocity.append(check_input_float('Initial Z Velocity: ', 'retry', 'stop'))
                    inputted_data.append(velocity)
                    
                spin.append(check_input_float('Initial X Spin: ', 'retry', 'stop'))
                spin.append(check_input_float('Initial Y Spin: ', 'retry', 'stop'))
                spin.append(check_input_float('Initial Z Spin: ', 'retry', 'stop'))
                inputted_data.append(spin)
                
                if(('retry' in inputted_data) or ('retry' in position) or ('retry' in velocity) or ('retry' in spin)):
                    inputted_data = []
                    position = []
                    velocity = []
                    spin = []
                elif(('stop' in inputted_data) or ('stop' in position) or ('stop' in velocity) or ('stop' in spin)):
                    retry = False
                    stop = True
                else:
                    if(particle_type == 'Fixed'):
                        particles.append(FixedParticle(*inputted_data, t_step=.1))
                    else:
                        particles.append(MovingParticle(*inputted_data, t_step=.1))
                    
                    inputted_data = []
                    position = []
                    velocity = []
                    spin = []
                    
                    label = JLabel('Would You Like to Make Another Particle?', JLabel.CENTER)
                    label.setFont(Font('Arial', Font.PLAIN, 35))
                    next = JOptionPane.showConfirmDialog(frame, label, '', JOptionPane.YES_NO_OPTION)
                    if(next == 1):
                        retry = False
                        stop = True
    
    return particles


def convert_coord(coord, line_length, max_size):
    """Converts real coords into pixel coords"""
    trans_coord = [0, 0, 0]
    line_length = float(line_length)
    trans_coord[0] = coord[0] * (line_length / (2 * max_size))
    trans_coord[1] = coord[2] * (-line_length / (2 * max_size))
    trans_coord[2] = coord[1] * (line_length / (2 * max_size))
    
    return trans_coord


def find_maximums(particles):
    """Finds max size of grid, max radius, and max charge"""
    radii = []
    for n in particles:
        radii.append(n.radius)
    max_radius = float(max(radii) + .0001)
    
    charges = []
    for n in particles:
        charges.append(abs(n.charge))
    max_charge = max(charges) + .00000000000000000001
    
    ranges = []
    max_start_positions = []
    for n in particles:
        position = n.position
        
        velocity = n.velocity
        velocity = float(vector_math.magnitude(velocity))
        
        acceleration = n.acceleration
        acceleration = float(vector_math.magnitude(acceleration))
        
        ranges.append((velocity * 1.2) + (.5 * acceleration * 1.44))
        
        for i in position:
            max_start_positions.append(abs(i))

    max_start_position = float(max(max_start_positions))
    max_size = float(max(ranges) + 1.2*max_start_position + 1)
    
    return max_size, max_radius, max_charge


def check_in_bounds(position, line_length):
    """Checks that particle is in bounds"""
    result = True
    for n in range(len(position)):
        if(abs(position[n]) > (line_length/2)):
            position[n] = (position[n] / abs(position[n])) * (line_length / 2)
            result = False
    return result


def draw_particles(particles, max_size, max_radius, max_charge, line_length):
    """Draws each particle in position, determines size and color using comparison to max radius and charge"""
    # Centers at origin
    translate(line_length/2, line_length/2, line_length/2)
    
    for n in particles:
        position = n.position
        angular_position = n.angular_position
        
        position = convert_coord(position, line_length, max_size)
        angular_position = list(map(lambda x: x % (2*PI), angular_position))
        
        if(not n.texture_data):
            stroke(150)
            if(n.charge < 0):
                fill(0, 100, int(-255 * (float(n.charge) / max_charge)))
            else:
                fill(int(255 * (float(n.charge) / max_charge)), 100, 0)
        else:
            noStroke()
            fill(255)
    
        if(check_in_bounds(position, line_length)):  
            particle_object = createShape(SPHERE, int(30 * (float(n.radius) / max_radius)))
        else:
            particle_object = createShape(BOX, int(30 * (float(n.radius) / max_radius)))
            
        if(n.texture_data):
            particle_object.setTexture(n.texture_data)
        
        pushMatrix()
        translate(*position)
        rotateX(angular_position[0])
        rotateY(angular_position[1])
        rotateZ(angular_position[2])
        shape(particle_object)
        popMatrix()
    
