"""
This file contains various shapes used in cropping. Typically, each shape contains the parameters necessary to describe the shape.
"""
from PIL import Image, ImageDraw
import numpy as np

OPTIMIZE_THRESHOLD = 200000 # This (250kP or 0.25 MP) is the size above which we resize the image before displaying

class Rectangle:
    """
    Defines the rectangle class. Each rectangle is described by shape, a 4-element tuple - (colstart, rowstart, width, height). Origin of the rectangle is the same as the image origin, typically the top left point with x axis increasing from left to right and y axis increasing from top to bottom (reverse). If the origin of the cropped image is different, shape will follow axis of the cropped image.
    """
    def __init__(self, x_size, y_size):
        """
        Parses slider inputs into the relevant parameters to describe the rectangle. For rectangle, these are 
        colstart, rowstart, width, height
        * Assumes a top-left origin for the image
        """
        # Parses the slider inputs
        colstart= x_size[0]
        width = x_size[1]-x_size[0]
        rowstart = im.size[1]-y_size[1]
        height = y_size[1]-y_size[0]
        # Assigns the shape params to the class property
		self.shape = (colstart, rowstart, width, height)
        
        
	def convert_sliders_to_shape_params(self, x_size, y_size):
        """
        Parses slider inputs into the relevant parameters to describe the rectangle. For rectangle, these are 
        colstart, rowstart, width, height
        * Assumes a top-left origin for the image
        """
        # Parses the slider inputs
        colstart= x_size[0]
        width = x_size[1]-x_size[0]
        rowstart = im.size[1]-y_size[1]
        height = y_size[1]-y_size[0]
        # Assigns the shape params to the class property
		self.shape = (colstart, rowstart, width, height)
        
	def get_shape(self):
		return self.shape
    
    def draw(self, img):
        """
        Draws a rectangle on the provided PIL Image (img), based on self.shape
        """
        draw = ImageDraw.draw(img)
        line_width = int(np.min(im_draw.size)/150)
        draw.rectangle((colstart, rowstart, colstart+width, rowstart+height), width=line_width)
        
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
        line_width = int(np.min(im_draw.size)/150)
        colstart, rowstart, width, height = self.shape
        draw.rectangle((colstart, rowstart, colstart+width, rowstart+height), width=line_width)
    
    def plot(self, img, optimize):
        """
        Plots the shape on an img and displays the shape on an optimized (or not) version of the ellipse:
        arguments:
        img - a PIL Image object
        optimize - a bool indicator for whether the plotting should be optimized for render times
        """
        if optimize and (img.size[0]*img.size[1]>OPTIMIZE_THRESHOLD): 
            # Scale down the image
            scale_factor = np.sqrt(img.size[0]*img.size[1]/OPTIMIZE_THRESHOLD)
            im_res = img.resize([int(s/scale_factor) for s in im_draw.size])
            display(im_res)
        else:
            display(im_draw)
            
        
        
