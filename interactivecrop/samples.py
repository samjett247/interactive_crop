from PIL import Image
import numpy as np
import os

dirname = os.path.dirname(__file__)
PATH_TO_SAMPLES = os.path.join(dirname, 'image_samples/')
SAMPLES = ['bird.jpg', 'castle.jpg', 'rhino.jpg', 'statue.jpg', 'tower.jpg']

sample_images = [np.array(Image.open(PATH_TO_SAMPLES+im)) for im in SAMPLES] 
sample_names = [i[:-4].title() for i in SAMPLES]
