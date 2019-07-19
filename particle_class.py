import math
import vector_math


class Particle:
    def __init__(self, mass, charge, radius, init_pos, init_vel, init_spin, t_step, texture_data):
        self.mass = mass
        self.charge = charge
        self.radius = radius

        self.position = init_pos
        self.velocity = init_vel
        self.acceleration = [0, 0, 0]

        self.angular_position = [0, 0, 0]
        self.angular_velocity = init_spin
        self.angular_acceleration = [0, 0, 0]

        self.t_step = t_step
        self.texture_data = self.add_texture(texture_data)
        
    def add_texture(self, texture_data):
        if(texture_data):
            return loadImage(texture_data)
        else:
            return None
        
    def get_position(self):
        position = self.position
        return position

    def get_velocity(self):
        velocity = self.velocity
        return velocity

    def get_acceleration(self):
        acceleration = self.acceleration
        return acceleration

    def get_angular_position(self):
        angular_position = self.angular_position
        return angular_position

    def get_angular_velocity(self):
        angular_velocity = self.angular_velocity
        return angular_velocity

    def get_angular_acceleration(self):
        angular_acceleration = self.angular_acceleration
        return angular_acceleration

    def get_magnetic_moment(self):
        """Finds magnetic dipole moment"""
        # Gets moment magnitude and angles
        angular_vel_magnitude = vector_math.magnitude(self.get_angular_velocity())
        magnitude = .2 * self.charge * angular_vel_magnitude * (self.radius ** 2)

        xy_spin = 0
        for i in range(2):
            xy_spin += self.get_angular_velocity()[i] ** 2
        xy_spin = xy_spin ** .5
        angular_phi = math.atan2(self.get_angular_velocity()[2], xy_spin)

        angular_theta = math.atan2(self.get_angular_velocity()[1], self.get_angular_velocity()[0])

        # Determines moment
        magnetic_moment = [0, 0, 0]
        magnetic_moment[0] = magnitude * math.sin(angular_phi) * math.cos(angular_theta)
        magnetic_moment[1] = magnitude * math.sin(angular_phi) * math.sin(angular_theta)
        magnetic_moment[2] = magnitude * math.cos(angular_phi)
        return magnetic_moment

    def get_magnetic_field(self, radius, distance):
        """Finds the magnetic field produced by dipole moment and moving charge"""
        mu = 4 * math.pi * (10 ** -7)

        # Created by spin
        moment = self.get_magnetic_moment()
        k1 = (.75 * mu * vector_math.dot_prod(radius, moment)) / (math.pi * (distance ** 3))
        v1 = vector_math.scalar_mult(k1, radius)

        k2 = mu / (4 * math.pi * (distance ** 3))
        v2 = vector_math.scalar_mult(k2, moment)

        spin_field = vector_math.subtract(v1, v2)

        # Created by translation
        k3 = (mu * self.charge) / (4 * math.pi * (distance ** 3))
        v3 = vector_math.cross_prod(self.get_velocity(), radius)

        translation_field = vector_math.scalar_mult(k3, v3)

        field = vector_math.add_vect(spin_field, translation_field)

        return field

    def set_acceleration(self, particles):
        """Sets acceleration using gravitational and electromagnetic forces"""
        g = 6.67408 * (10 ** -11)
        k = 8.98755 * (10 ** 9)

        acceleration = [0, 0, 0]
        for n in particles:
            # Radius between particles split by dimension
            radius = [0, 0, 0]
            for i in range(3):
                radius[i] += n.get_position()[i] - self.get_position()[i] + .00001

            # Magnitude of radius
            distance = vector_math.magnitude(radius)

            # Magnitude of acceleration combined with angles to find acceleration
            accel_magnitude = ((g * n.mass) / (distance ** 3)) - (
                        (k * n.charge * self.charge) / (self.mass * (distance ** 3)))
            added_acceleration = vector_math.scalar_mult(accel_magnitude, radius)
            acceleration = vector_math.add_vect(acceleration, added_acceleration)

            # Force from Magnetic Field
            field = n.get_magnetic_field(radius, distance)
            vector = vector_math.cross_prod(self.get_velocity(), field)
            mag_acceleration = vector_math.scalar_mult((self.charge / self.mass), vector)

            acceleration = vector_math.add_vect(acceleration, mag_acceleration)

        self.acceleration = acceleration

    def collision(self, particles):
        """Sees if a collision occured and return between which objects the collision occurs"""
        collision_list = []
        for n in particles:
            distance = vector_math.magnitude(vector_math.subtract(n.get_position(), self.get_position()))
            radius_sum = n.radius + self.radius
            if(distance < radius_sum):
                collision_list.append(n)
                
        return collision_list
    
    def perform_collision(self, collision_list, particles):
        """Performs an elastic collision"""
        for n in collision_list:
            if((self.get_velocity() != [0, 0, 0]) and (n.get_velocity() != [0, 0, 0])):
                radius = vector_math.subtract(self.get_position(), n.get_position())
                distance = vector_math.magnitude(radius)
                k1 = ((2 * n.mass) / (self.mass + n.mass)) * ((vector_math.dot_prod(vector_math.subtract(self.get_velocity(), n.get_velocity()), radius)) / (distance ** 2))
                k2 = ((2 * self.mass) / (self.mass + n.mass)) * ((vector_math.dot_prod(vector_math.subtract(n.get_velocity(), self.get_velocity()), radius)) / (distance ** 2))
                
                v1 = vector_math.scalar_mult(k1, radius)
                v2 = vector_math.scalar_mult(k2, radius)
                
                self.velocity = vector_math.subtract(self.get_velocity(), v1)
                n.velocity = vector_math.subtract(n.get_velocity(), v2)
                
                self.position = vector_math.add_vect(self.get_position(), vector_math.scalar_mult(self.t_step, self.get_velocity()))
                n.position = vector_math.add_vect(n.get_position(), vector_math.scalar_mult(n.t_step, n.get_velocity()))
                
                self.set_acceleration(particles)
                n.set_acceleration(particles)
            elif(self.velocity != [0, 0, 0]):
                self.velocity = vector_math.scalar_mult(-1, self.get_velocity())
                self.position = vector_math.add_vect(self.get_position(), vector_math.scalar_mult(self.t_step, self.get_velocity()))
                self.set_acceleration(particles)
            elif(n.velocity != [0, 0, 0]):
                n.velocity = vector_math.scalar_mult(-1, n.get_velocity())
                n.position = vector_math.add_vect(n.get_position(), vector_math.scalar_mult(n.t_step, n.get_velocity()))
                n.set_acceleration(particles)

    def set_velocity(self, particles):
        """Sets velocity using acceleration, previous velocity, and time_step"""
        collision_list = self.collision(particles)
        if(collision_list):
            self.perform_collision(collision_list, particles)
        else:
            velocity = self.get_velocity()
            for n in range(3):
                velocity[n] += self.get_acceleration()[n] * self.t_step

            self.velocity = velocity

    def set_position(self):
        """Sets position using velocity, acceleration, previous position, and time step"""
        position = self.get_position()
        for n in range(3):
            position[n] += (self.get_velocity()[n] * self.t_step) + (.5 * self.get_acceleration()[n] * (self.t_step ** 2))

        self.position = position

    def set_angular_acceleration(self, particles):
        """Sets angular acceleration using magnetic torque"""
        dipole_moment = self.get_magnetic_moment()
        angular_acceleration = [0, 0, 0]
        for n in particles:
            # Radius between particles split by dimension
            radius = [0, 0, 0]
            for i in range(3):
                radius[i] += n.get_position()[i] - self.get_position()[i] + .00001

            # Magnitude of radius
            distance = vector_math.magnitude(radius)
            
            field = n.get_magnetic_field(radius, distance)
            vector = vector_math.cross_prod(dipole_moment, field)
            mag_angular_acceleration = vector_math.scalar_mult((1 / (self.mass * (self.radius ** 2))), vector)

            angular_acceleration = vector_math.add_vect(angular_acceleration, mag_angular_acceleration)

        self.angular_acceleration = angular_acceleration

    def set_angular_velocity(self):
        """Sets angular velocity using angular acceleration, previous velocity, and time step"""
        angular_velocity = self.get_angular_velocity()
        for n in range(3):
            angular_velocity[n] += self.get_angular_acceleration()[n] * self.t_step

        self.angular_velocity = angular_velocity

    def set_angular_position(self):
        """Sets angular position using angular velocity, acceleration, previous position, and time step"""
        angular_position = self.get_angular_position()
        for n in range(3):
            angular_position[n] += (self.get_angular_velocity()[n] * self.t_step) + (.5 * self.get_angular_acceleration()[n] * (self.t_step ** 2))

        self.angular_position = angular_position


class MovingParticle(Particle):
    def __init__(self, mass, charge, radius, init_pos, init_vel, init_spin, t_step, texture_data = None):
        Particle.__init__(self, mass, charge, radius, init_pos, init_vel, init_spin, t_step, texture_data)

    def do_motion(self, particles):
        """Updates all motion vectors"""
        self.set_acceleration(particles)
        self.set_velocity(particles)
        self.set_position()

        self.set_angular_acceleration(particles)
        self.set_angular_velocity()
        self.set_angular_position()


class FixedParticle(Particle):
    def __init__(self, mass, charge, radius, init_pos, init_spin, t_step, texture_data = None):
        Particle.__init__(self, mass, charge, radius, init_pos, [0, 0, 0], init_spin, t_step, texture_data)

    def do_motion(self, particles):
        """Updates all motion vectors"""
        self.set_angular_acceleration(particles)
        self.set_angular_velocity()
        self.set_angular_position()
        
        self.velocity = [0, 0, 0]
        
