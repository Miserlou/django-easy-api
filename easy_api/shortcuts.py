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
    import simplejson as json # Support for older Python

from .dumper import DataDumper # Probably can be deprecated.
from dicttoxml import dicttoxml as dict2xml # Requirest dict2xml dep.
from xml.dom.minidom import parseString # For prettyfication

def render_to_easy_api_response(*args, **kwargs):
    """
    Returns a HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    """
    httpresponse_kwargs = {'content_type': kwargs.pop('content_type', None)}

    # This is really quite hacky.
    context = kwargs.pop('context_instance')
    processors = context.context_processors
    request = processors['django.core.context_processors.request']['request']

    if request.GET.has_key('api'):
        api_type = request.GET['api']

        # This is dirty, but direct indexing doesn't work here because technically we're using variable length arguments.
        # I'm assuming that the parameters dictionary will always be the last non-named argument. This is likely a bug.
        # Better solutions welcome!
        for arg in args:
            passed = arg

        dump_me = {}

        for key in passed.keys():
            value = passed[key]
            dump_me[key] = dump_object(value)

        if api_type == 'xml':

            # The XML parser chokes on spaces in key names.
            # This recursively replaces them with underscores.
            def replace_spaces(dump_me):
                new = {}
                for k, v in dump_me.iteritems():
                    if isinstance(v, dict):
                        v = replace_spaces(v)
                    new[k.replace(' ', '_')] = v
                return new

            new = replace_spaces(dump_me)
            dump_me = dict2xml(new)

            dom = parseString(dump_me)  # I love pretty APIs!
            pretty = dom.toprettyxml()
            return HttpResponse(pretty, content_type='application/xml')
        else:    
            dump_me = json.dumps(dump_me, indent=2)  # Indents for pretty
            return HttpResponse(dump_me, content_type='application/json')


    return HttpResponse(loader.render_to_string(*args, **kwargs), **httpresponse_kwargs)

def render_to_response(*args, **kwargs):
    """
    This is just a wrapper around render_to_easy_api_response to make it easier to use as a drop-in replacement.
    """

    return render_to_easy_api_response(*args, **kwargs)

###
#
# Serializers stuff. Mostly stolen from what I did making django-knockout-modeler.
#
##

def dump_object(queryset):

    # Nasty.
    if str(type(queryset)) != "<class 'django.db.models.query.QuerySet'>":
        d = DataDumper()
        ret = d.dump(queryset)
        return ret

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
        return json.loads(json.dumps(modelNameData, default=dthandler))
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
