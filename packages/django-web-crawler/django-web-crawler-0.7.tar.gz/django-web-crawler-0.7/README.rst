===========
Web Crawler
===========

Crawler is a Django app to help connect to a website and gather as much links as you want.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "gatherlinks" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'gatherlinks',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('crawl/', include('crawl.urls')),

3. Run ``python manage.py migrate`` to create the polls models.

4. Visit http://127.0.0.1:8000/crawl/ to input the domain name of the website you want to gather it's links.