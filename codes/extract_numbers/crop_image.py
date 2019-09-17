#a class for store some info of blob
class Blob:

    def __init__(self,points,angle,cropped,slope):
        self.points = points
        self.angle = angle
        self.cropped = cropped


    def getPoints(self):
        return self.points

    def getAngle(self):
        return self.angle

    def getCropped(self):
        return self.cropped

    def setCropped(self, cropped):
        self.cropped = cropped

    def getSlope(self):
        return self.slope

    def setSlope(self, slope):
        self.slope = slope
