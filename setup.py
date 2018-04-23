from setuptools import setup

NAME = 'iherb'
DESCRIPTION = 'Get products from iHerb'
URL = 'https://github.com/liamcryan/iherb'
EMAIL = 'data.handyman.01@gmail.com'
AUTHOR = 'Liam Cryan'
VERSION = '0.0.0'
LICENSE = "MIT"


setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=DESCRIPTION,
      url=URL,
      download_url="https://github.com/liamcryan/iherb/archive/0.0.0.tar.gz",
      license=LICENSE,
      author=AUTHOR,
      author_email=EMAIL,
      packages=["iherb"],
      install_requires=["requests-html==0.9.0"],
      include_package_data=True,
      dependency_links=["http://github.com/liamcryan/requests-html/tarball/master#egg=requests-html-0.9.0"],
      keywords="iherb products",
      python_requires='>=3.6.0',
      classifiers=["Programming Language :: Python :: 3.6"])
