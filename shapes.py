"""
This file contains various shapes used in cropping. Typically, each shape contains the parameters necessary to describe the shape.
"""
from PIL import Image, ImageDraw
import numpy as np

OPTIMIZE_THRESHOLD = 200000 # This (200kP or 0.20 MP) is the size above which we resize the image before displaying, if optimize

class Rectangle:
    """
    Defines the rectangle class. Each rectangle is described by shape, a 4-element tuple - (colstart, rowstart, width, height). Origin of the rectangle is the same as the image origin, typically the top left point with x axis increasing from left to right and y axis increasing from top to bottom (reverse). If the origin of the cropped image is different, shape will follow axis of the cropped image.
    """
    def __init__(self, x_size, y_size, image):
        """
        Parses slider inputs into the relevant parameters to describe the rectangle. For rectangle, these are 
        colstart, rowstart, width, height
        * Assumes a top-left origin for the image
        """
        # Parses the slider inputs
        colstart= x_size[0]
        width = x_size[1]-x_size[0]
        rowstart = image.size[1]-y_size[1]
        height = y_size[1]-y_size[0]

        # Assigns the shape params to the class property
        self.shape = (colstart, rowstart, width, height)
        # Assigns the im to self.image
        self.image = image
        # Keeps a count of the number of shape adjustments
        self.adjustment_count = 1
        
        
    def convert_sliders_to_shape_params(self, x_size, y_size):
        """
        Parses slider inputs into the relevant parameters to describe the rectangle. For rectangle, these are 
        colstart, rowstart, width, height
        * Assumes a top-left origin for the image
        """
        # Parses the slider inputs
        colstart= x_size[0]
        width = x_size[1]-x_size[0]
        rowstart = self.image.size[1]-y_size[1]
        height = y_size[1]-y_size[0]
        # Assigns the shape params to the class property
        self.shape = (colstart, rowstart, width, height)
        self.adjustment_count +=1
        
    def get_shape(self):
        return self.shape

    def plot(self, optimize):
        """
        Plots the shape on an img and displays the shape on an optimized (or not) version of the ellipse:
        arguments:
        img - a PIL Image object
        optimize - a bool indicator for whether the plotting should be optimized for render times
        """
        img = self.image
        if optimize and (img.size[0]*img.size[1]>OPTIMIZE_THRESHOLD): 
            # Scale down the image
            scale_factor = np.sqrt(img.size[0]*img.size[1]/OPTIMIZE_THRESHOLD)
            im_res = img.resize([int(s/scale_factor) for s in img.size])
            display(im_res)
        else:
            display(self.image)
    
    def draw(self):
        """
        Draws a rectangle on self.image based on self.shape, only if the adjustment_count is sufficiently high, because the initialization involves some adjustments
        """
        if self.adjustment_count >3:
            draw = ImageDraw.Draw(self.image)
            line_width = int(np.min(self.image.size)/150)
            colstart, rowstart, width, height = self.shape
            draw.rectangle((colstart, rowstart, colstart+width, rowstart+height), width=line_width, outline='white')

    def erase_drawing(self, im):
        self.image = im.copy()
        
class Ellipse:
    """
    Defines the Ellipse class. Each ellipse is described by self.shape, a 4-element tuple - (x0, y0, x1, y1), where (x0,y0) are the coords of top left point of bounding box, and x1,y1 are the coords of bottom right point of bounding box. Origin of the rectangle is the same as the image origin, typically the top left point with x axis increasing from left to right and y axis increasing from top to bottom (reverse). If the origin of the cropped image is different, shape will follow axis of the cropped image.
    """
    def convert_sliders_to_shape_params(self, x_size, y_size):
        """
        Parses slider inputs into the relevant parameters to describe the ellipse. For ellipse, these are a 4-element tuple - (x0,         y0, x1, y1), where (x0,y0) are the coords of top left point of bounding box, and x1,y1 are the coords of bottom right             point of bounding box. 
        * Assumes a top-left origin for the image
        """
        # Parses the slider inputs
        x0= x_size[0]
        x1= x_size[1]
        y0 = im.size[1]-y_size[1]
        y1 = im.size[1]-y_size[0]
        # Assigns the shape params to the class property
        self.shape = (x0,y0,x1,y1)
        
    def get_shape(self):
        return self.shape
    
    def draw(self, img):
        """
        Draws a rectangle on the provided PIL Image (img), based on self.shape
        """
        draw = ImageDraw.draw(img)
        line_width = int(np.min(self.image.size)/150)
        colstart, rowstart, width, height = self.shape
        draw.rectangle((colstart, rowstart, colstart+width, rowstart+height), width=line_width)
    

            
        
        
