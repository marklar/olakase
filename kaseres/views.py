from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.template import Context, loader

from kaseres.models import Task, User, TaskList
from kaseres.accepts import accepts_json, accepts_html, accepts_xml
from kaseres.responses import json_models_response, json_obj_response, xml_models_response, xml_obj_response, make_response

# Check for desired format: HTML or JSON.
# If JSON, return data.  If HTML, use template.

def restify(f):
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

SORT_ATTRS = [
    ('Title', 'title'),
    ('Due', 'due_date'),
    ('Priority', 'priority'),
    ('Completed?', 'is_completed')
]

@require_safe
@restify
def index(request):
    """
    If ajax, return the HTML for just the list of tasks.
    """
    # hi_pri_tasks = Task.objects.order_by('-priority')[:5]
    attr = request.GET['attr'] if 'attr' in request.GET else 'priority'
    tasks = Task.objects.order_by('-' + attr)
    return {
        'models': tasks,
        'template': get_index_template(request.is_ajax()),
        'context': {'tasks': tasks, 'sort_attrs': SORT_ATTRS}
    }

@require_POST
def create_task(request):
    """
    Response: "201 Created" with a Location header
    containing the URL to the newly created resource.
    """
    # task_list_id
    # title
    # details
    # due_date
    # is_completed
    # priority

    # create the task
    # use data: request.POST
    task_list = TaskList.objects.get(1)
    task = task_list.task_set.create(request.POST)
    task.save()

    # FIXME -- return the *HTML* for the new task.
    res_url = ''
    return json_model_response(task, status=201, location=res_url)

    # tasks = Task.objects.all()
    # template = loader.get_template('tasks/all_tasks.html')
    # context = Context({'tasks': tasks})
    # return make_response(
    #     template.render(context), 'text/html', status, location)


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
    task = Task.objects.get(task_id)
    # if accepts_json(request):
    if True:
        return json_models_response(task)
    elif accepts_xml(request):
        return xml_models_response(task)
    else:
        return HttpResponse('<h1>HTML</h1>')


@require_http_methods(['PUT'])
def update_task(request, task_id):
    pass


@require_http_methods(['DELETE'])
def delete_task(request, task_id):
    Task.objects.get(id=task_id).delete()
    return HttpResponse('')

# -- helpers --

def get_index_template(is_ajax):
    if is_ajax:
        return 'tasks/all_tasks.html'
    else:
        return 'tasks/index.html'

def all_tasks_html(status=200, location=None):
    # how sorted?
    tasks = Task.objects.all()
    template = loader.get_template('tasks/all_tasks.html')
    context = Context({'tasks': tasks})
    return make_response(
        template.render(context), 'text/html', status, location)

