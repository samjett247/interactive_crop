import ipywidgets as widgets
from ipywidgets import interact, interact_manual, interactive, Layout, GridBox, fixed
from matplotlib import pyplot as plt
from matplotlib import patches
from IPython.display import display
import time
from PIL import Image
from sys import exit as sysexit
import numpy as np

# Change default output size of matplotlib figures
plt.rcParams['figure.figsize'] = (13.0, 11.0)
plt.rcParams['figure.dpi'] = 100 # default for me was 75

checked_crop = False
im = 0
def main(image_list, shape = 'Rectangle', 
    callback = lambda x,y: print('{}: {}'.format(x,y))):
    """
    This function takes a list of images and allows the user interactively crop these images through a vertical range slider and a horizontal range slider. Once the crop size is accepted, the callback kwarg will be called and provided the name of the cropped image (from image_list) and the shape of the cropped_image.

    Arguments: 
    image_list - A list of image names
    shape - The desired type of crop shape
    callback - The function to call after the crop size is accepted

    Returns: 
    coord_dict - A dict mapping image names to cropped coordinates
    """
    coord_dict = {}
    fig, axs = plt.subplots(1)
    fig.set_size_inches(13,11)

    def show_image(image_name):
        """
        Shows the image at the desired size
        """
        # Read image from file and convert to ndarray
        print(coord_dict)
        im = Image.open(image_name).convert('L')
        im_arr = np.array(im)
        # Adjust the slider limits based on the pixel size of the image
        print('1')
        x_size_selector.value = (im_arr.shape[1]/3, 2*im_arr.shape[1]/3)
        print('2')
        x_size_selector.min, x_size_selector.max = 0, im_arr.shape[1]
        print('3')
        x_size_selector.value = (im_arr.shape[0]/3, 2*im_arr.shape[0]/3)
        print('4')
        y_size_selector.min, y_size_selector.max = 0, im_arr.shape[0]
        fig, axs = plt.gcf(), plt.gca()
        axs.set_title(image_name)
        axs.imshow(im, cmap = 'gray')
        plt.show()

        def add_crop_patch(x_size, y_size):
            # parse inputs to crop fxn
            colstart= x_size[0]
            width = x_size[1]-x_size[0]
            rowstart = im_arr.shape[0]-y_size[1]
            height = y_size[1]-y_size[0]
            # Get the axs to add the patch to
            axs = plt.gca()
            rect = patches.Rectangle((colstart, rowstart), width,height, linewidth=3, edgecolor='r', facecolor='none')
            axs.add_patch(rect)
        interact(add_crop_patch, x_size=x_mod, y_size = y_mod)

        # Click button to save params
        save_crop_sizes=interact.options(manual=True, manual_name="Save Crop Sizes")
        @save_crop_sizes
        def on_button_click(image_name=fixed(image_name), size = fixed((colstart, rowstart, width, height))):
            """
            This will handle the onbutton click event of the 
            """
            callback(image_name, size)
            coord_dict[image_name] = size
            im_index = image_list.index(image_name)
            if im_index != len(image_list)-1:
                image_selector.value = image_list[im_index+1]
            else:
                print('Made it through all the tests; Stopping execution now.')
                sysexit()
            time.sleep(5) # Change this to change how long you have to look at the cropped results
            return
        return

    # Define test_name selector
    image_selector = widgets.Dropdown(
    options=image_list,
    value=image_list[0],
    description='Test Name:',
    disabled=False,
    continuous_update=False,
    layout=Layout(grid_area='test_name')
    )

    # Define selectors for int range sliders
    x_size_selector = widgets.IntRangeSlider(
        value=(400,800),
        min=0,
        max=2448,
        step=1,
        description='Width: ',
        continuous_update=True,
        orientation='horizontal',
        layout=Layout(width='auto', grid_area='width')
    )

    y_size_selector = widgets.IntRangeSlider(
        value=(400, 800),
        min=0,
        max=2050,
        step=1,
        description='Height: ',
        continuous_update=True,
        orientation='vertical',
        readout=True,
        layout=Layout(width='auto',height = 'auto', grid_area='height', display='hidden')
    )
    x_mod = widgets.IntRangeSlider(
        value=(800,1400),
        min=0,
        max=2448,
        layout=Layout(width='0%',height='0%', visibility='hidden')
    )
    y_mod = widgets.IntRangeSlider(
        value=(400, 800),
        min=0,
        max=2050,
        layout=Layout(width='0%',height='0%', visibility='hidden')
    )
    im_mod = widgets.Select(
    options=image_list,
    value=image_list[0],
    layout=Layout(width='0%',height='0%', visibility='hidden')
    )

    # Link the x,y,im selectors to mod widgets for the interactive function
    widgetLinkx = widgets.jslink((x_size_selector, 'value'), (x_mod, 'value'))
    widgetLinky = widgets.jslink((y_size_selector, 'value'), (y_mod, 'value'))
    widgetLinktn = widgets.jslink((image_selector, 'index'), (im_mod, 'index'))

    cropper = interactive(show_image, image_name =image_selector, layout=Layout(width='auto', grid_area='main'));
    return GridBox(children=[image_selector,x_size_selector,y_size_selector, cropper ],
        layout=Layout(
            width='80%',
            grid_template_rows='10% 90%',
            grid_template_columns='30% 70%',
            grid_template_areas='''
            "test_name width"
            "height main "
            ''')
       )
    return coord_dict

if __name__ == "__main__":
    main(['Test_419', 'Test_420', 'Test_421', 'Test_422'])
