import collections
from django.http import HttpResponse
from django.core import serializers

def json_models_response(models, status=200, location=None):
    json = serializers.serialize('json', make_iterable(models))
    return json_response(json, status, location)

def json_obj_response(obj, status=200, location=None):
    json = json.dumps(obj)
    return json_response(json, status, location)

def xml_models_response(models, status=200, location=None):
    xml = serializers.serialize('xml', make_iterable(models))
    return xml_response(xml, status, location)

# -- FIXME --
def xml_obj_response(obj, status=200, location=None):
    pass
    # xml = serializers.serialize('xml', obj)
    xml = 'foo'
    return xml_response(xml, status, location)

# -----

def json_response(json, status, location):
    return make_response(json, 'application/json', status, location)

def xml_response(xml, status, location):
    return make_response(xml, 'application/xml', status, location)

def make_response(text, mimetype, status, location):
    r = HttpResponse(
        text,
        mimetype=mimetype,
        status=status
    )
    if location is not None:
        r['Location'] = location
    return r

def make_iterable(xs):
    return xs if isinstance(xs, collections.Iterable) else [xs]
