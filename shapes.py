"""
This file contains various shapes used in cropping. Typically, each shape contains the parameters necessary to describe the shape.
"""
from PIL import Image, ImageDraw
import numpy as np

OPTIMIZE_THRESHOLD = 200000 # This (200kP or 0.20 MP) is the size above which we resize the image before displaying, if optimize

class Shape:
    """
    Defines methods and properties for the basic Shape class. Specific shapes extend this class
    """
    def __init__(self, x_size, y_size, image, crop_shape):
        """
        Parses slider inputs into the relevant parameters to describe the rectangle. For rectangle, these are 
        colstart, rowstart, width, height
        * Assumes a top-left origin for the image
        """
        # Keeps a count of the number of shape adjustments for initial plotting
        self.adjustment_count = 0
        # Assigns the im to self.image
        self.image = image
        self.convert_sliders_to_shape_params(x_size, y_size)
        self.shape =crop_shape
        
    def get_size(self):
        return self.size
    def get_crop_shape(self):
        return self.shape

    def display(self, optimize):
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

    def erase_drawing_on_image(self, im):
        """
        Resets self.image to the provided image, essentially erasing any drawings applied
        """
        self.image = im.copy()
       
class Rectangle(Shape):
    """
    Defines the Rectangle class. Each rectangle is described by shape, a 4element tuple - (colstart, rowstart, width, height). Origin of the rectangle is the top left point with x axis increasing from left to right and y axis increasing from top to bottom (reverse). 
    """
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
        self.size = (colstart, rowstart, width, height)
        self.adjustment_count +=1

    def draw(self):
        """
        Draws a rectangle on self.image based on self.size, only if the adjustment_count is sufficiently high, because the initialization involves some adjustments
        """
        if self.adjustment_count >3:
            draw = ImageDraw.Draw(self.image)
            line_width = int(np.min(self.image.size)/150)
            colstart, rowstart, width, height = self.size
            draw.rectangle((colstart, rowstart, colstart+width, rowstart+height), width=line_width, outline='white')

class Ellipse(Shape):
    """
    Defines the Ellipse class. Each ellipse is described by self.size, a 4-element tuple - (x0, y0, x1, y1), where (x0,y0) are the coords of top left point of bounding box, and x1,y1 are the coords of bottom right point of bounding box. Origin of the rectangle is the same as the image origin, typically the top left point with x axis increasing from left to right and y axis increasing from top to bottom (reverse). If the origin of the cropped image is different, shape will follow axis of the cropped image.
    """
    def convert_sliders_to_shape_params(self, x_size, y_size):
        """
        Parses slider inputs into the relevant parameters to describe the ellipse. For ellipse, these are a 4-element tuple - (x0,y0, x1, y1), where (x0,y0) are the coords of top left point of bounding box, and (x1,y1) are the coords of bottom right point of bounding box. 
        * Assumes a top-left origin for the image
        """
        # Parses the slider inputs
        x0= x_size[0]
        x1= x_size[1]
        y0 = self.image.size[1]-y_size[1]
        y1 = self.image.size[1]-y_size[0]
        # Assigns the size params to the class property
        self.size = (x0,y0,x1,y1)
        self.adjustment_count +=1
    
    def draw(self):
        """
        Draws a rectangle on the self.image based on self.size, only if the adjustment_count is sufficiently high, because the initialization involves some adjustments
        """
        if self.adjustment_count>3:
            draw = ImageDraw.Draw(self.image)
            line_width = int(np.min(self.image.size)/150)
            x0,y0,x1,y1 = self.size
            draw.ellipse((x0,y0,x1,y1), width=line_width, outline='white')

class Triangle(Shape):
    """
    Defines the Triangle class. Each triangle is isosceles and described by self.size, a 4-element tuple - (x0, y0, x1, y1), where x0 describes the left-most point of the triangle,y0 describes the highest point of the triangle, and (x1,y1) are the coords of bottom right point of triangle. Origin of the rectangle is the same as the image origin, typically the top left point with x axis increasing from left to right and y axis increasing from top to bottom (reverse). If the origin of the cropped image is different, shape will follow axis of the cropped image.
    """
    def convert_sliders_to_shape_params(self, x_size, y_size):
        """
        Parses slider inputs into the relevant parameters to describe the triangle. See class description for point description.
        """
        # Parses the slider inputs
        x0= x_size[0]
        x1= x_size[1]
        y0 = self.image.size[1]-y_size[1]
        y1 = self.image.size[1]-y_size[0]
        # Assigns the size params to the class property
        self.size = (x0,y0,x1,y1)
        self.adjustment_count +=1

    def draw(self):
        """
        Draws a triangle on the self.image based on self.size, only if the adjustment_count is sufficiently high, because the initialization involves some adjustments
        """
        if self.adjustment_count>3:
            draw = ImageDraw.Draw(self.image)
            line_width = int(np.min(self.image.size)/150)
            x0,y0,x1,y1 = self.size
            # Convert point 0,1 to point A,B,C of isosceles triangle
            xa, ya = x0,y1
            xb, yb = x1,y1
            xc, yc = ((x0+x1)/2),y0 
            draw.line([(xa,ya), (xb,yb), (xc,yc), (xa,ya)], width=line_width, fill='white')
