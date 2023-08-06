import os
import re
import inspect

from distutils.core import setup

def get_path():
    globalPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    return globalPath

def read(fname):
    __file__ = get_path()
    return open(os.path.join(__file__, fname)).read()

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
  name = 'gimpysolver',         # How you named your package folder (MyLib)
  packages = ['gimpysolver'],   # Chose the same as "name"
  version = '0.0.8',      # Start with a small number and increase it with every change you make
  license='gpl-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = ('This is a simple and specific solver to gimpy captcha types like SEACE PORTAL. The model has been trained with 4000 images and 92 porcent of accuracy.'),   # Give a short description about your library
  long_description=read("README.rst"),
  long_description_content_type = "text/markdown",
  author = 'Cesar Cortez',                   # Type in your name
  author_email = 'cc@digitaliatec.com',      # Type in your E-Mail
  url = "http://github.com/CesarCort/gimpysolver",   # Provide either the link to your github or to your website
  project_urls={
        "Bug Tracker": "http://github.com/CesarCort/gimpysolver/issues",
    },
  keywords = ['CAPTCHA', 'CAPTCHASOLVER', 'GIMPY','GIMPYSOLVER','SOLVER'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
         'keras==2.7.0',
	'opencv-python==4.5.5',
	'importlib',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License (GPL)',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)