# Blatantly stolen from:
# https://djangosnippets.org/snippets/1162/

import types
from django.db import models
from django.utils import simplejson as json
from django.core.serializers.json import DateTimeAwareJSONEncoder
from decimal import *

class DataDumper:
    fields = {}
    def selectObjectFields(self,objectType,fields = []):
        self.fields[objectType] = fields

    def dump(self,data,format='xml'):
        """
        The main issues with django's default json serializer is that properties that
        had been added to a object dynamically are being ignored (and it also has 
        problems with some models).
        """
    
        def _any(data):
            ret = None
            if type(data) is types.ListType:
                ret = _list(data)
            elif type(data) is types.DictType:
                ret = _dict(data)
            elif isinstance(data, Decimal):
                # json.dumps() cant handle Decimal
                ret = str(data)
            elif isinstance(data, models.query.QuerySet):
                # Actually its the same as a list ...
                ret = _list(data)
            elif isinstance(data, models.Model):
                ret = _model(data)
            else:
                ret = data
            return ret
        
        def _model(data):
            ret = {}
            # If we only have a model, we only want to encode the fields.
            objType = data.__class__.__name__
            for f in data._meta.fields:
                if (self.fields[objType]) and (f.attname in self.fields[objType]):
                    ret[f.attname] = _any(getattr(data, f.attname))
            # And additionally encode arbitrary properties that had been added.
            fields = dir(data.__class__) + ret.keys()
            add_ons = [k for k in dir(data) if k not in fields]
            for k in add_ons:
                if (self.fields[objType]) and (k in self.fields[objType]):
                    ret[k] = _any(getattr(data, k))
            return ret
        def _list(data):
            ret = []
            for v in data:
                ret.append(_any(v))
            return ret
        
        def _dict(data):
            ret = {}
            for k,v in data.items():
                ret[k] = _any(v)
            return ret
        
        ret = _any(data)
        return ret
