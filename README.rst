=====
iherb
=====

Get products & details from iHerb.

One year later
==============

It's been a year since this library was written.  Amazingly it still works.  However, there is a caveat
in which some of the attributes scraped return None.  This is because iherb has likely been changing the
placement of their product details.

Also, if you run into a SSL error, you can comment out line 6 in url.py.


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