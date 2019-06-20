import ipywidgets as widgets

def get_main_widgets(image_list, continuous_update):
    # Define test_name selector
    image_selector = widgets.Dropdown(
    options=image_list,
    value=image_list[0],
    description='Image Name:',
    disabled=False,
    continuous_update=continuous_update,
    layout=widgets.Layout(grid_area='im_selector')
    )
    # Define selectors for int range sliders; We'll define value and max, min 
    # once we know image size
    x_size_selector = widgets.IntRangeSlider(
        step=1,
        description='Width:',
        continuous_update=continuous_update,
        orientation='horizontal',
        layout=widgets.Layout(width='auto', grid_area='width')
    )

    y_size_selector = widgets.IntRangeSlider(
        step=1,
        description='Height:',
        continuous_update=continuous_update,
        orientation='vertical',
        layout=widgets.Layout(width='auto',height = 'auto', grid_area='height')
    )
    return image_selector, x_size_selector, y_size_selector
    
def get_hidden_widgets(image_list, continuous_update):
    
    # Define mod sliders for cropping function; We'll define value and max, min 
    # once we know image size
    x_mod = widgets.IntRangeSlider(
        layout=widgets.Layout(width='0%',height='0%', visibility='hidden')
    )
    y_mod = widgets.IntRangeSlider(
        continuous_update=continuous_update,
        step=1,
        layout=widgets.Layout(width='0%',height='0%', visibility='hidden')
    )
    im_mod = widgets.Select(
        options=image_list,
        value=image_list[0],
        layout=widgets.Layout(width='0%',height='0%', visibility='hidden')
    )
    return im_mod, x_mod,y_mod