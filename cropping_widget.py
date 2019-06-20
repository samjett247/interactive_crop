import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
import time
from PIL import Image, ImageDraw
from sys import exit as sysexit
from shapes import Rectangle, Ellipse
import numpy as np
import widgets_helper
import pprint
from ipyexit import exit

def main(image_list, crop_shape = 'Rectangle', continuous_update=True, optimize = True,
    callback = lambda x,y: print('{}: {}'.format(x,y))):
    """
    This function takes a list of images and allows the user interactively crop these images through a vertical range slider and a horizontal range slider. Once the crop size is accepted, the callback kwarg will be called and provided the name of the cropped image (from image_list) and the shape of the cropped_image.

    Arguments: 
    image_list - A list of image names
    
    shape - The desired type of crop shape
    continuous_update (default: True) - Bool to indicate whether the plot should dynamically re-render as the user drags the slider, or should wait til slider release to rerender
    optimize (default: True)- Bool to indicate whether the program can optimize for faster rendering of crop boxes, including displaying grayscale images
    outline_color (default: red) - 
    callback - The function to call after the crop size is accepted (via button click)

    Returns: 
    coord_dict - A dict mapping image names to cropped coordinates
    """
    # Need these to retain the global scope
    coord_dict = {}
    SHAPE_DICT = {'Rectangle':Rectangle,'Ellipse':Ellipse} # shape arg mapping
    
    def show_image(image_name):
        """
        Shows the image at the desired size
        """
        # Clear output from prior image
        clear_output()
        # Read image from file
        im = Image.open(image_name)
        if optimize:
            im = im.convert('L')
            im = Image.fromarray(np.array(im).astype(np.uint8))
            
        # Create copy of image to draw on
        display(HTML('<h3 style="margin:5px;text-align:center">'+image_name+'</h3>'))
        
        # Instantiate shape object
        shape = SHAPE_DICT[crop_shape](x_mod.value, y_mod.value, im.copy())
        
        # Adjust the slider limits based on the pixel size of the image
        x_size_selector.min, x_size_selector.max = 0, im.size[0]
        x_mod.min, x_mod.max = 0, im.size[0]
        y_size_selector.min, y_size_selector.max = 0, im.size[1]
        y_mod.min, y_mod.max = 0, im.size[1]
        y_size_selector.value = (int(im.size[1]/3), int(2*im.size[1]/3))
        x_size_selector.value = (int(im.size[0]/3), int(2*im.size[0]/3))
        
        def add_crop_patch(x_size, y_size):
            """
            Adds the crop pa
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
            # Get the shape of the accepted crop size
            crop_size = shape.get_size()
            # Call the callback function, providing the image_name and the crop size
            callback(image_name, crop_size)
            coord_dict[image_name] = crop_size
            # Move to the next image_name or close
            im_ind = image_list.index(image_name)
            if im_ind != len(image_list)-1:
                image_selector.value = image_list[im_ind+1]
            else:
                print('\n Made it through all the tests. \nPrinting cropped results below.\n')
                print('\n\n')
                pprint.pprint(coord_dict)
                print('\n\n')
            time.sleep(2) # Change this to change how long you have to look at the cropped results
            return
        return
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
            grid_template_rows='10% 90%',
            grid_template_columns='30% 70%',
            grid_template_areas='''
            "im_selector width"
            "height main "
            '''))
    return main_widget

if __name__ == '__main__':
    print('Please call main() function and provide arguments.')
