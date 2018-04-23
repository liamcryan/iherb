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

    pip install git+https://github.com/liamcryan/iherb --process-dependency-links --trusted-host github.com

Note: requests-html did not paginate correctly and I forked a version which this package uses.  Running the above
command does not install my version of requests-html, so this library won't work yet for >24 products per category.

