import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='crop-interactive',  
     version='0.0.1',
     scripts=['crop-interactive'] ,
     author="Sam Jett",
     author_email="samjett247@gmail.com",
     description="An interactive image cropping tool for Jupyter Notebooks",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/samjett247/crop-interactive",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: GNU Public License (GPL)",
         "Operating System :: OS Independent",
     ],
 )
