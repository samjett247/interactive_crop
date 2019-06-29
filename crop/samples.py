from PIL import Image
import os
import numpy as np

PATH_TO_SAMPLES = 'crop/examples/image_samples'

sample_images = [np.array(Image.open(PATH_TO_SAMPLES+'/'+im)) for im in os.listdir(PATH_TO_SAMPLES)] 
sample_names = [i[:-4].title() for i in os.listdir(PATH_TO_SAMPLES)]

if __name__=='__main__':
    print(sample_images)