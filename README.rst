=====
iherb
=====

Get products from iHerb.

This library was created to test out requests-html as well as learn about 'yield' vs 'return'.

Usage
=====

.. code-block:: pycon

    >>> import iherb
    >>> for product in iherb.supplements(limit=5):
    ...     print(product)

iHerb has many categories and there is an api to obtain products from each of them.


Installation
============

.. code-block::

    pip install git+https://github.com/liamcryan/requests-html.git
    pip install git+https://github.com/liamcryan/iherb.git

Notes
=====

* I could not seem to properly specify dependency_link in setup.py file, hence the need for 2 pip installs
* The version of requests-html is a fork of the original and the library will not work correctly with the
original if requesting more than 24 items per category.
