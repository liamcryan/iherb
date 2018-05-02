=====
iherb
=====

Get products & details from iHerb.

Usage
=====

.. code-block:: pycon

    >>> import iherb
    >>> for product in iherb.supplements(limit=5):
    ...     print(product)

iHerb has many categories and there is an api to obtain products from each of them.  Be smart and limit your calls
using the limit argument.


Installation
============

.. code-block::

    pip install git+https://github.com/liamcryan/requests-html.git
    pip install git+https://github.com/liamcryan/iherb.git

Notes
=====

* I could not seem to properly specify dependency_link in setup.py file, hence the need for 2 pip installs.
* The version of requests-html is a fork of the original requests-html library.  Slight modifications have been made
  because requests-html was not paginating correctly.


iherb robots.txt file
=====================

User-agent: *
Disallow: /EditCart
Disallow: /WishList
Disallow: /Logout
Disallow: /Checkout
Disallow: /ordersummary
Disallow: /NotificationList
Disallow: /ChangePassword
Disallow: /AddressBook
Disallow: /Profile
Disallow: /PersonalInfo
Disallow: /Pro/RecentProductSelection
Disallow: /Pro/VisitedProduct
Disallow: /Pro/GetFeatured
Disallow: /Pro/CustomerBought
Disallow: /Pro/EnableCustomerHistory
Disallow: /Pro/DisableCustomerHistory
Disallow: /Pro/ReviewFeedback
Disallow: /Pro/ViewSwitcher
Disallow: /Pro/Maintentance
Disallow: /Pro/ReportAbuse
Disallow: /Pro/CustomerViewed
Disallow: /Search
Disallow: /search

user-agent: msnbot
Crawl-delay: 2