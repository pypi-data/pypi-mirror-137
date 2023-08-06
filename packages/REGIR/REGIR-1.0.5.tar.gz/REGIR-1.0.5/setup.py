

import setuptools
#https://realpython.com/pypi-publish-python-package/
#https://dzone.com/articles/executable-package-pip-install
#https://medium.com/@atharvakulkarniamk/creating-a-pypi-package-on-windows-9254716bb3f8

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='REGIR',  
     version='1.0.5',
     author="Aurelien Pelissier",
     author_email="aurelien.pelissier.38@gmail.com",
     description="An algorithm for non-Markovian stochastic simulation",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/Aurelien-Pelissier/REGIR/",
     packages=setuptools.find_packages(),
     keywords = ['Gillespie', 'modeling', 'stochastic', 'simulation'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )