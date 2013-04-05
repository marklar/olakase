
def accepts_json(request):
    return accepts(request, 'application/json')

def accepts_xml(request):
    return accepts(request, 'application/xhtml+xml')

def accepts_html(request):
    return accepts(request, 'text/html')

# -- private --

def accepts(request, mimetype):
    return mimetype in get_mimetypes(request)

def get_mimetypes(request):
    attr = 'accepted_mimetypes'
    if getattr(request, attr, None) is None:
        vals = get_vals_from_header(request.META['HTTP_ACCEPT'])
        setattr(request, attr, vals)
    return getattr(request, attr)

def get_vals_from_header(str):
    return [a.split(';')[0] for a in str.split(',')]
