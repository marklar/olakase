#!/usr/bin/python
import sys
import requests

base_url = 'http://127.0.0.1:8000/kaseres/tasks/'

def m_get(path, params={}, headers={}):
    return requests.get(base_url + path, params=params, headers=headers)

def m_post(path, params={}, headers={}):
    return requests.post(base_url + path, params=params, headers=headers)

def m_delete(path, headers={}):
    return requests.delete(base_url + path, headers=headers)

def out(r):
    print r.status_code
    print r.text

def p_get(mime, path, params={}):
    r = m_get(path, params=params, headers=get_headers(mime))
    out(r)

def p_post(mime, path, params={}):
    r = m_post(path, params=params, headers=get_headers(mime))
    out(r)

def p_delete(mime, path):
    r = m_delete(path, headers=get_headers(mime))
    out(r)

def get_headers(mime):
    if mime not in ['xml', 'json', 'html']:
        print "What mime?: %s" % mime
        return {}

    if mime == 'xml':
        v = 'application/xhtml+xml'
    elif mime == 'json':
        v= 'application/json'
    elif mime == 'html':
        v = 'text/html'
    else:
        # Should never get here.
        v = 'text/html'
    return {'accept': v}

#-----------

def index(mime):
    p_get(mime, '')

def create(mime, params={'title': 'my new task', 'details': ''}):
    """ Uses some default values for the Task. """
    p_post(mime, 'create/', params=params)

def read(mime, id):
    path = "%d/read/" % id
    p_get(mime, path)

def update(mime, id, params={'title': 'brand new title'}):
    path = "%d/update/" % id
    p_post(mime, path, params=params)

def delete(mime, id):
    path = "%d/delete/" % id
    p_delete(mime, path)

#-----------

def get_id():
    return int(sys.argv[3])

try:
    verb = sys.argv[1]
    mime = sys.argv[2]
    if verb == 'create':
        create(mime, {'title': sys.argv[3], 'details': ''})
    elif verb == 'read':
        read(mime, get_id())
    elif verb == 'update':
        update(mime, get_id(), {'title': sys.argv[4]})
    elif verb == 'delete':
        delete(mime, get_id())
    else:
        print "What verb?"
except IndexError:
    print "usage:"
    print "   %s create <mime> [<title>]" % sys.argv[0]
    print "   %s read   <mime> <id>" % sys.argv[0]
    print "   %s update <mime> <id> <title>" % sys.argv[0]
    print "   %s delete <mime> <id>" % sys.argv[0]
               
               
