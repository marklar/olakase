from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.template import Context, loader

from kaseres.models import Task, User, TaskList
from kaseres.accepts import accepts_json, accepts_html, accepts_xml
from kaseres.responses import json_models_response, json_obj_response, xml_models_response, xml_obj_response

# Check for desired format: HTML or JSON.
# If JSON, return data.  If HTML, use template.

def blurfl(f):
    def wrapper(request):
        d = f(request)

        # check whether 'obj' or 'models'
        # in order to call the right fn

        if accepts_json(request):
            return json_models_response(d['models'])
        # elif accepts_xml(request):
        elif False:
            return xml_models_response(d['models'])
        else:
            template = loader.get_template(d['template'])
            context = Context(d['context'])
            return HttpResponse(template.render(context))
    return wrapper

# the view fn must return:
#   { 'models': models,
#     'template': STR,
#     'context': {},
#     'status': 200,   # optional
#     'location: url   # optional
#   }
#

@require_safe
@blurfl
def index(request):
    hi_pri_tasks = Task.objects.order_by('-priority')[:5]
    return {
        'models': hi_pri_tasks,
        'template': 'tasks/index.html',
        'context': {'tasks': hi_pri_tasks}
    }

# @require_POST
def create_task(request):
    """
    Response: "201 Created" with a Location header
    containing the URL to the newly created resource.
    """
    # task_list_id
    # title
    # body
    # due_date
    # is_completed
    # priority

    task_list = TaskList.objects.get(1)
    task_list.task_set.create()

    res_url = ''
    return {
        'obj': request.GET,
        
    }
    if accepts_json(request):
        return json_obj_response(request.GET, status=201, location=res_url)
    elif accepts_xml(request):
        return xml_obj_response(request.GET, status=201, location=res_url)
    else:
        return HttpResponse('<h1>HTML</h1>')


@require_safe
def index_old(request):
    hi_pri_tasks = Task.objects.order_by('-priority')[:5]
    if accepts_json(request):
        return json_models_response(hi_pri_tasks)
    elif False: # accepts_xml(request):
        return xml_models_response(hi_pri_tasks)
    else:
        template = loader.get_template('tasks/index.html')
        context = Context({'tasks': hi_pri_tasks})
        return HttpResponse(template.render(context))


# @require_POST
def create_task(request):
    """
    Response: "201 Created" with a Location header
    containing the URL to the newly created resource.
    """
    # task_list_id
    # title
    # body
    # due_date
    # is_completed
    # priority
    res_url = ''
    if accepts_json(request):
        return json_obj_response(request.GET, status=201, location=res_url)
    elif accepts_xml(request):
        return xml_obj_response(request.GET, status=201, location=res_url)
    else:
        return HttpResponse('<h1>HTML</h1>')


@require_safe
def read_task(request, task_id):
    task = Task.objects.get(id=task_id)
    # if accepts_json(request):
    if True:
        return json_models_response(task)
    elif accepts_xml(request):
        return xml_models_response(task)
    else:
        return HttpResponse('<h1>HTML</h1>')


@require_http_methods(['PUT'])
def update_task(request, task_id):
    # task_id is a STRING
    pass


@require_http_methods(['DELETE'])
def delete_task(request, task_id):
    # task_id is a STRING
    pass

