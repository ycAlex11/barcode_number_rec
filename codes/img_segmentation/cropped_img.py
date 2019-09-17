'''
create a class for each blob, store their location and height
'''
class Cropped_image:

    def __init__(self,points,height):
        self.points = points
        self.height = height

    def get_points(self):
        return self.points

    def get_height(self):
        return self.height
