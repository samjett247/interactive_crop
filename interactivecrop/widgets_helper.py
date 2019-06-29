import numpy as np

import ipywidgets as widgets
from PIL import Image


def create_image_name_LUT(image_list, image_name_list, optimize):
    """
    Parses the input lists and creates an dict for image lookup based on the image_name. If optimize, converts all types to uint8 and grayscale
    Returns:
    list of image names
    Dict where keys are lists of image names and values are PIL images
    """
    # Check if image_name_list was provided
    if image_name_list:
        if len(image_list)!=len(image_name_list):
            raise Exception('The length of provided image_list was {} while the length of image_name_list was {}.'.format(len(image_list), len(image_name_list)))
        images_named = True
    else:
        images_named= False
        
    # Handles the cases where arguments were provided in str form
    if all(isinstance(image, str) for image in image_list):
        if images_named:
            if optimize:
                return image_name_list, {image_name_list[i]:Image.fromarray(np.array(Image.open(image_list[i])).astype(np.uint8)).convert('L') for i in range(len(image_list))}
            else:
                return image_name_list, {image_name_list[i]:Image.open(image_list[i]) for i in range(len(image_list))}
        else: 
            if optimize:
                 return image_list, {image_list[i]:Image.fromarray(np.array(Image.open(image_list[i])).astype(np.uint8)).convert('L') for i in range(len(image_list))}
            else:    
                return image_list, {image_list[i]:Image.open(image_list[i]) for i in range(len(image_list))} 
        
    # Handles the case where arguments were nd.arrays
    elif all(isinstance(image, np.ndarray) for image in image_list):
        if images_named:
            if optimize:
                return image_name_list, {image_name_list[i]:Image.fromarray(image_list[i].astype(np.uint8)).convert('L') for i in range(len(image_list))}
            else:
                return image_name_list, {image_name_list[i]:Image.fromarray(image_list[i]) for i in range(len(image_list))}
        else:
            if optimize:
                return ['Image {}'.format(i) for i in range(len(image_list))], {'Image {}'.format(i):Image.fromarray(image_list[i].astype(np.uint8)).convert('L') for i in range(len(image_list))}
            else:
                return ['Image {}'.format(i) for i in range(len(image_list))], {'Image {}'.format(i):Image.fromarray(image_list[i]) for i in range(len(image_list))}
    else:
        raise Exception('Image list elements are not in the allowable string or np.ndarray formats')


def get_main_widgets(image_list, continuous_update):
    # Define test_name selector
    image_selector = widgets.Dropdown(
    options=image_list,
    value=image_list[0],
    description='Img Name:',
    continuous_update=continuous_update,
    layout=widgets.Layout(width='100%', grid_area='im_selector')
    )
    # Define selectors for int range sliders; We'll define value and max, min 
    # once we know image size
    x_size_selector = widgets.IntRangeSlider(
        step=1,
        description='Width:',
        continuous_update=continuous_update,
        orientation='horizontal',
        layout=widgets.Layout(width='98%', grid_area='width')
    )

    y_size_selector = widgets.IntRangeSlider(
        step=1,
        description='Height:',
        continuous_update=continuous_update,
        orientation='vertical',
        layout=widgets.Layout(height='90%',width = 'auto', grid_area='height')
    )
    return image_selector, x_size_selector, y_size_selector
    
def get_hidden_widgets(image_list, continuous_update):
    
    # Define mod sliders for cropping function; We'll define value and max, min 
    # once we know image size
    x_mod = widgets.IntRangeSlider(
        layout=widgets.Layout(display='none')
    )
    y_mod = widgets.IntRangeSlider(
        continuous_update=continuous_update,
        step=1,
        layout=widgets.Layout(display='none')
    )
    im_mod = widgets.Select(
        options=image_list,
        value=image_list[0],
        layout=widgets.Layout(width='0%',height='0%', visibility='hidden')
    )
    return im_mod, x_mod,y_mod