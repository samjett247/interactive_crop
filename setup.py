import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='interactivecrop',  
     version='0.0.5',
     author="Sam Jett",
     author_email="samjett247@gmail.com",
     description="An interactive image cropping tool for Jupyter Notebooks in Python",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/samjett247/interactive_crop",
     packages=setuptools.find_packages(),
     install_requires=[
        'pandas',
        'numpy',
        'pillow',
        'ipywidgets',
        'ipython'],
     classifiers=[
         "Programming Language :: Python :: 3",
         'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
         "Operating System :: OS Independent",
     ],
 )
