class Graphics:
    def __init__(self, line_length, line_num):
        self.line_length = line_length
        self.line_num = line_num
        

    def draw_pyramid(self, py_size):
        """Draws a pyramid out from the center"""
        strokeWeight(1)
        stroke(50)
        
        rectMode(CENTER)
        square(0, 0, py_size)
        
        beginShape()
        vertex(-py_size/2, -py_size/2, 0)
        vertex(0, 0, 2*py_size)
        vertex(-py_size/2, py_size/2, 0)
        vertex(-py_size/2, -py_size/2, 0)
        endShape()
    
        beginShape()
        vertex(py_size/2, -py_size/2, 0)
        vertex(0, 0, 2*py_size)
        vertex(py_size/2, py_size/2, 0)
        vertex(py_size/2, -py_size/2, 0)
        endShape()
        
        beginShape()
        vertex(-py_size/2, -py_size/2, 0)
        vertex(0, 0, 2*py_size)
        vertex(py_size/2, -py_size/2, 0)
        vertex(-py_size/2, -py_size/2, 0)
        endShape()
        
        beginShape()
        vertex(-py_size/2, py_size/2, 0)
        vertex(0, 0, 2*py_size)
        vertex(py_size/2, py_size/2, 0)
        vertex(-py_size/2, py_size/2, 0)
        endShape()
        
        strokeWeight(4)
    
    
    def create_axes(self):
        """Creates x, y, and z axes"""
        strokeWeight(4)
        # z axis
        stroke(100, 255, 100)
        fill(100, 255, 100)
        line(0, self.line_length/2, 0, -self.line_length/2)
        pushMatrix()
        translate(0, -self.line_length/2, 0)
        rotateX(PI/2)
        self.draw_pyramid(30)
        popMatrix()
        
        # y axis
        stroke(255, 75, 75)
        fill(255, 75, 75)
        line(-self.line_length/2, 0, self.line_length/2, 0)
        pushMatrix()
        translate(self.line_length/2, 0, 0)
        rotateY(PI/2)
        self.draw_pyramid(30)
        popMatrix()
        
        # x axis
        pushMatrix()
        rotateX(PI/2)
        stroke(75, 75, 255)
        fill(75, 75, 255)
        line(0, -self.line_length/2, 0, self.line_length/2)
        pushMatrix()
        translate(0, self.line_length/2, 0)
        rotateX(-PI/2)
        self.draw_pyramid(30)
        popMatrix()
        popMatrix()
        
        strokeWeight(.25)
        stroke(200)
        
    
    def orient_grid(self, angleX, angleY):
        """Orientates grid based on origin of grid"""
        translate(self.line_length / 2, self.line_length / 2, self.line_length / 2)
        rotateY(angleX)
        rotateX(-angleY)
        self.create_axes()
        translate(-self.line_length/2, -self.line_length/2, -self.line_length/2)
    
    
    def create_grid(self):
        """Creates Grid"""
        # X-Y Planes of Grid
        for n in range(self.line_num):
            pushMatrix()
            translate(0, 0, n*(self.line_length/(self.line_num-1)))
            for i in range(self.line_num):
                pushMatrix()
                translate(0, i*(self.line_length/(self.line_num-1)), 0)
                line(0, 0, self.line_length, 0)
                popMatrix()
            
            for i in range(self.line_num):
                pushMatrix()
                translate(i*(self.line_length/(self.line_num-1)), 0, 0)
                line(0, 0, 0, self.line_length)
                popMatrix()
            popMatrix()
    
        # X-Z Planes in Grid
        for n in range(self.line_num):
            pushMatrix()
            translate(n*(self.line_length/(self.line_num-1)), 0, 0)
            for i in range(self.line_num):
                pushMatrix()
                translate(0, i*(self.line_length/(self.line_num-1)), 0)
                rotateX(PI/2)
                line(0, 0, 0, self.line_length)
                popMatrix()
            popMatrix()
            

class Rotations:
    def __init__(self):
        self.mouse_position = [0, 0]
        self.angleX = 0
        self.angleY = 0
        
    def get_mouse_position(self):
        mouse_position = self.mouse_position
        return mouse_position
        
    def update_mouse_position(self, _mouseX, _mouseY):
        """Updates the position of the mouse"""
        self.mouse_position = [_mouseX, _mouseY]
        
    def update_angles(self, _width, _height, _mouseX, _mouseY):
        """Updates angles based on change of mouse position"""
        changeX = float(_mouseX - self.get_mouse_position()[0])
        changeY = float(_mouseY - self.get_mouse_position()[1])
        
        self.angleX += 2*PI*(changeX / _width)
        self.angleY += 2*PI*(changeY / _height)
        
        self.update_mouse_position(_mouseX, _mouseY)
        
