
from distutils.core import setup

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
  name = 'gimpysolver',         # How you named your package folder (MyLib)
  packages = ['gimpysolver'],   # Chose the same as "name"
  version = '0.0.3',      # Start with a small number and increase it with every change you make
  license='gpl-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This is a simple and specific solver to gimpy captcha types like SEACE PORTAL. The model has been trained with 4000 images and 92 porcent of accuracy.',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type = "text/markdown",
  author = 'César Cortez',                   # Type in your name
  author_email = 'cc@digitaliatec.com',      # Type in your E-Mail
  url = 'https://github.com/CesarCort/gimpysolver',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/CesarCort/gimpysolver/archive/refs/heads/main.zip',    # I explain this later on
  keywords = ['CAPTCHA', 'CAPTCHASOLVER', 'GIMPY','GIMPYSOLVER','SOLVER'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'keras',
          'io',
	   'PIL',
	'opencv-python',
'importlib',
'io'
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