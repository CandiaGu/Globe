#altered from Point3D() class by Leonel Machava
import math

#x, y, and z only vary between -1 and 1
class Point3D:

	#changed
    def __init__(self, angle1, angle2):

        rad1, rad2 = math.radians(angle1), math.radians(angle2)

    	#from 3D Calc lel
        self.x, self.y, self.z = math.cos(rad1)*math.sin(rad2), -math.sin(rad1)*math.sin(rad2), math.cos(rad2)
        # where angle1 is the angle in the xy plane and the angle2 is the 
      			# angle between the z coordinate line and the xy plane
        self.angle1, self.angle2 = angle1, angle2 

        self.roundToNearestTenth()
 
    def rotateX(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """

        cosa = math.cos(math.radians(angle))
        sina = math.sin(math.radians(angle))
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        self.y, self.z = y, z
        if self.x == 0:
        	self.x = 0.0001
        if self.x > 0:
        	self.angle1 = math.degrees(math.atan(self.y/self.x))
        else:
 	        self.angle1 = 180+math.degrees(math.atan(self.y/self.x))

        if self.angle1<0:
            self.angle1 +=360
        if -1<=z<1:
        	self.angle2 = math.degrees(math.acos(z))

        self.roundToNearestTenth()
    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        cosa = math.cos(math.radians(angle))
        sina = math.sin(math.radians(angle))
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        self.z = z
        self.x = x
        if self.x == 0:
        	self.x == 0.0001
        
        if self.x > 0:
        	self.angle1 = math.degrees(math.atan(self.y/self.x))
        else:
            self.angle1 = 180+math.degrees(math.atan(self.y/self.x))

        if self.angle1<0:
        	self.angle1 +=360
        #print(z)
        if -1<=z<1:
        	self.angle2 = math.degrees(math.acos(z))

        self.roundToNearestTenth()
 
    def rotateZ(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        self.x = x
        self.y = y

        self.angle1 += angle

        self.roundToNearestTenth()
 
    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2

        return (x,y)

    def roundToNearestTenth(self):
    	self.x = round(self.x,5)
    	self.y = round(self.y,5)
    	self.z = round(self.z,5)


