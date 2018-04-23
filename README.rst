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

pip install git+https://github.com/liamcryan/iherb --process-dependency-links

