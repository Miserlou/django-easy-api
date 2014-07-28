"""

This is based off of Django's own shorcuts.py which provides render_to_response.

The key function here is easy_api_render_to_response()

"""
from django.template import loader, RequestContext
from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.db.models.base import ModelBase
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.core import urlresolvers
from django.utils import six

import datetime
try:
    import json
except Exception, e:
    import simplejson as json

def render_to_easy_api_response(*args, **kwargs):
    """
    Returns a HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    """
    httpresponse_kwargs = {'content_type': kwargs.pop('content_type', None)}

    context = kwargs.pop('context_instance')
    processors = context.context_processors
    request = processors['django.core.context_processors.request']['request']

    if request.GET.has_key('api'):
        api_type = request.GET['api']

        for arg in args:
            passed = arg

        dump_me = ''

        for key in passed.keys():
            value = passed[key]
            dump_me = dump_me + dump_object(value)

        return HttpResponse(dump_me, content_type='application/json')


    return HttpResponse(loader.render_to_string(*args, **kwargs), **httpresponse_kwargs)

def render_to_response(*args, **kwargs):
    """
    This is just a wrapper around render_to_easy_api_response to make it easier to use as a drop-in replacement.
    """

    return render_to_easy_api_response(*args, **kwargs)

def dump_object(queryset):

    try:
        modelName = queryset[0].__class__.__name__    
        modelNameData = []

        fields = get_fields(queryset[0])

        for obj in queryset:
            temp_dict = dict()
            for field in fields:
                try:
                    attribute = getattr(obj, str(field))

                    # Should sanitization be up to the API consumer? Probably.

                    # if not safe:
                    #     if isinstance(attribute, basestring):
                    #         attribute = cgi.escape(attribute)

                    temp_dict[field] = attribute
                except Exception, e:
                    continue
            modelNameData.append(temp_dict)

        dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime)  or isinstance(obj, datetime.date) else None
        return json.dumps(modelNameData, default=dthandler)
    except Exception, e:
        return ''

def get_fields(model):

    try:
        if hasattr(model, "easy_api_fields"):
            fields = model.easy_api_fields()
        else:
            try:
                fields = model.to_dict().keys()
            except Exception, e:
                fields = model._meta.get_all_field_names()

        return fields

    # Crash proofing
    except Exception, e:
        return []
