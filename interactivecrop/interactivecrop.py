import time
import pprint
from sys import exit as sysexit

import numpy as np
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output, Markdown

from .shapes import Rectangle, Ellipse, Triangle
from . import widgets_helper

def default_callback(im_name, im_obj):
    print('{}: {}'.format(im_name,im_obj.get_size()))
    time.sleep(1.5)
    
def main(image_list, image_name_list = [], crop_shape = 'Rectangle', continuous_update=True, optimize = True,
    callback = default_callback):
    """
    This function takes a list of images and allows the user interactively crop these images through a vertical range slider and a horizontal range slider. Once the crop size is accepted, the callback kwarg will be called and provided the name of the cropped image (from image_list) and the shape of the cropped_image.

    Required Arguments: 
    image_list(list of str or nd.array objects) - A list of image filenames or a list of images as np.ndarray objects. 

    Optional Arguments:
    continuous_update (default: True) - Bool to indicate whether the plot should dynamically re-render as the user drags the slider, or should wait til slider release to rerender.

    image_names_list(list, default: []) - The names of the images, to use when displaying the images and to pass to callback function. Must have same length as image_list. Recommended, especially when providing nd.array objects in the image_list.

    crop_shape (str, default: Rectangle) - The desired type of crop shape; Current options - Rectangle, Ellipse, Triangle

    optimize (bool, default: True) - Indicates whether the program can optimize for faster updating of crop boxes, including displaying grayscale images and reducing pixel quality of display

    callback(function, default: prints the image name and crop size) - The function to call after the crop size is accepted via button click. The function receives the name of the image (or image index if image_list is np.ndarray objects) and the image object, defined in shapes.py. Crop size is available as a prop of the image object as img_obj.size. Similarly, modified PIL image is a prop at img_obj.image

    Returns: 
    cropping widget

    """
    # Need these to retain the global scope
    coord_dict = {}
    SHAPE_DICT = {'Rectangle':Rectangle,'Ellipse':Ellipse, 'Triangle':Triangle} # shape arg mapping
    def show_image(image_name):
        """
        Shows the image at the desired size.
        image_name: name of the image
        """
        # Clear output from prior image
        clear_output()
        
        # Get the image
        im = image_LUT[image_name]
            
        # Create copy of image to draw on
        display(HTML('<h3 style="margin:5px;text-align:left">'+image_name+'</h3>'))

        # Instantiate shape object
        shape = SHAPE_DICT[crop_shape](x_mod.value, y_mod.value, im.copy(), crop_shape)
        
        # Adjust the slider limits based on the pixel size of the image
        x_size_selector.min, x_size_selector.max = 0, im.size[0]
        x_mod.min, x_mod.max = 0, im.size[0]
        y_size_selector.min, y_size_selector.max = 0, im.size[1]
        y_mod.min, y_mod.max = 0, im.size[1]
        y_size_selector.value = (int(im.size[1]/3), int(2*im.size[1]/3))
        x_size_selector.value = (int(im.size[0]/3), int(2*im.size[0]/3))
        
        def add_crop_patch(x_size, y_size):
            """
            Adds the crop patch to the image.
            """
            # Ensure shape is up to date on slider changes
            shape.convert_sliders_to_shape_params(x_size, y_size)
            # Draw the shape on im_draw
            shape.draw()
            # Plot the shape on im_draw
            shape.display(optimize)
            shape.erase_drawing_on_image(im)
            
        widgets.interact(add_crop_patch, x_size=x_mod, y_size = y_mod)
        # Click button to save params
        save_crop_sizes=widgets.interact.options(manual=True, manual_name="Save Crop Sizes")
        @save_crop_sizes
        def on_button_click(image_name=widgets.fixed(image_name)):
            """
            This will handle the onbutton click event of the cropper.
            """
            # Call the callback function, providing the image_name and the crop size
            callback(image_name, shape)
            coord_dict[image_name] = shape.get_size()
            # Move to the next image_name or close
            im_ind = image_list.index(image_name)
            if im_ind != len(image_list)-1:
                image_selector.value = image_list[im_ind+1]
            else:
                print('\n Made it through all the tests.\nPrinting cropped results below.\n')
                print('\n\n')
                pprint.pprint(coord_dict)
                print('\n\n')
            return
        return
    # Create image LUT based on image_name arguments
    image_list, image_LUT = widgets_helper.create_image_name_LUT(image_list, image_name_list, optimize)
    
    # Build the image list based on the type of image_list
    image_selector, x_size_selector, y_size_selector = widgets_helper.get_main_widgets(image_list, continuous_update)
    im_mod, x_mod, y_mod = widgets_helper.get_hidden_widgets(image_list,continuous_update)
    
    # Link the x,y,im selectors to mod widgets for the interactive function
    widgetLinkx = widgets.jslink((x_size_selector, 'value'), (x_mod, 'value'))
    widgetLinky = widgets.jslink((y_size_selector, 'value'), (y_mod, 'value'))
    widgetLinktn = widgets.jslink((image_selector, 'index'), (im_mod, 'index'))

    cropper = widgets.interactive(show_image, image_name =im_mod, layout=widgets.Layout(width='auto', grid_area='main'));
    main_widget = widgets.GridBox(children=[image_selector,x_size_selector,y_size_selector, cropper ],
        layout=widgets.Layout(
            width='90%',
            height='100%',
            grid_template_rows='10% 90%',
            grid_template_columns='25% 75%',
            grid_template_areas='''
            "im_selector width"
            "height main "
            '''))

    return main_widget

if __name__ == '__main__':
    print('Call main() function of this module with provided image arguments.')
