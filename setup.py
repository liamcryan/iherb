from setuptools import setup

NAME = 'iherb'
DESCRIPTION = 'Get products from iHerb'
URL = 'https://github.com/liamcryan/iherb'
EMAIL = 'data.handyman.01@gmail.com'
AUTHOR = 'Liam Cryan'
VERSION = '0.0.1'
LICENSE = "MIT"

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=DESCRIPTION,
      url=URL,
      license=LICENSE,
      author=AUTHOR,
      author_email=EMAIL,
      packages=["iherb"],
      # dependency_links=["http://github.com/liamcryan/requests-html/tarball/master#egg=requests-html-0.9.0"],
      # install_requires=["requests-html==0.9.0"],
      include_package_data=True,
      keywords="iherb products",
      python_requires='>=3.6.0',
      classifiers=["Programming Language :: Python :: 3.6"])
