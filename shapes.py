"""
This file contains various shapes used in cropping. Typically, each shape contains the parameters necessary to describe the shape.
"""

class Rectangle:
"""
Defines the rectangle class. Each rectangle is described by shape, a 4-element tuple - (colstart, rowstart, width, height). Origin of the rectangle is the same as the image origin, typically the top left point with x axis increasing from left to right and y axis increasing from top to bottom (reverse). If the origin of the cropped image is different, shape will follow axis of the cropped image.
"""
	def __init__(self, colstart, rowstart, width, height):
		self.shape = colstart, rowstart, width, height
	def get_shape(self):
		return (colstart, rowstart, width, height)

