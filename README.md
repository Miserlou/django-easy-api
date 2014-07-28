![Easy peasy!](http://bitemeblog.files.wordpress.com/2011/08/3567green_pea.jpg)

django-easy-api
===============

**django_easy_api** lets you create an API for your Django project by changing only a single line of code! 

The easiest way to use **django_easy_api** is to simply replace render_to_response:

```python
# from django.shortcuts import render_to_response
from easy_api.shortcuts import render_to_response 
```

So if this returns a rendered HTML view:

    http://yoursite.com/item/23

then this returns a JSON serialized view of the same page:

    http://yoursite.com/item/23?api=json

and this returns an XML serialized view of the same page:

    http://yoursite.com/item/23?api=xml

Hooray! You literally don't have to do anything else.

## Installation

You know the drill:

    pip install django_easy_api

Then add it to your INSTALLED_APPS.

## Usage

The easiest way to use **django_easy_api** is to simply replace render_to_response:

```python
# from django.shortcuts import render_to_response
from easy_api.shortcuts import render_to_response 
```

Now, all of your views will have API versions as well!

If you only want to use **django_easy_api** for certain views, you can use it explicitly:

```python
    from easy_api.shortcuts import render_to_easy_api_response
```
and then use it in your view instead of render_to_response.

## Notes

Okay, okay, so it's not a FULL API. It's just for GETs. If you want a full-featured API, look at Django-Rest-Framework. However, if you just need a machine-readable version of your site, this is far and away the easiest way to do it!

### TODO:

* I don't know what it does for ForeignKeys.
* XML doesn't work yet.
* I haven't tested this in production.

