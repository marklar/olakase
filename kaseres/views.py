from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.template import Context, loader
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date

# from kaseres.models import Task, User, TaskList
from kaseres.models import Task
from kaseres.accepts import accepts_json, accepts_html, accepts_xml
from kaseres.responses import json_models_response, json_obj_response, xml_models_response, xml_obj_response, make_response

import logging
logger = logging.getLogger(__name__)


def restify(f):
    """
    the view fn must return:
    { 'models': models,
      'template': STR,
      'context': {},
      'status': 200,   # optional
      'location: url   # optional
    }
    """
    def wrapper(request):
        d = f(request)
        if accepts_html(request):
            return render(request, d['template'], d['context'])
        elif accepts_json(request):
            return json_models_response(d['models'])
        elif accepts_xml(request):
            return xml_models_response(d['models'])
        else:
            return render(request, d['template'], d['context'])
    return wrapper


SORT_ATTRS = [
    ('Title', 'title'),
    ('Due', 'due_date'),
    ('Priority', 'priority'),
    ('Done', 'is_completed')
]

@require_safe
@restify
def index(request):
    """
    If ajax, return the HTML for just the list of tasks.
    """
    tasks = Task.objects.order_by(get_sort(request.GET))
    return {
        'models': tasks,
        'template': get_index_template(request.is_ajax()),
        'context': {
            'tasks': tasks,
            'priorities': Task.PRIORITIES,
            'sort_attrs': SORT_ATTRS
        }
    }

@require_POST
def create_task(request):
    """
    Response: "201 Created" with a Location header
    containing the URL to the newly created resource.
    """
    task = create_task_from_data(request.REQUEST)
    # location = reverse('read_task', kwargs={'task_id': task.id})
    # location = reverse(views.read_task, kwargs={'task_id': task.id})
    # location = reverse('read_task') # , args=[task.id])
    location = 'What should this be?'
    if accepts_json(request):
        return json_models_response(task, status=201, location='')
    elif accepts_xml(request):
        return xml_models_response(task, status=201, location='')
    else:
        template = loader.get_template('tasks/one_task.html')
        context = Context({
            'task': task,
            'priorities': Task.PRIORITIES
        })
        return make_response(
            template.render(context), 'text/html', status=201, location='')
            

@require_safe
def read_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except ObjectDoesNotExist:
        # FIXME: change format.
        return HttpResponse('Does not exist.', status=404)

    if accepts_html(request):
        return render(request, 'tasks/one_task.html', {
            'task': task,
            'priorities': Task.PRIORITIES
        })
    elif accepts_xml(request):
        return xml_models_response(task)
    elif accepts_json(request):
        return json_models_response(task)
    else:
        return render(request, 'tasks/one_task.html', {'task': task})

@require_POST
def update_task(request, task_id):
    """
    Uses POST instead of PUT, as accessing POST data is easier
    than using request.raw_post_data or request.read().
    @require_http_methods(['PUT'])
    use tastypie: https://github.com/toastdriven/django-tastypie
    """
    try:
        task = Task.objects.get(id=task_id)
    except ObjectDoesNotExist:
        # FIXME: change format.
        return HttpResponse('Does not exist.', status=500)

    update_task_from_data(task, request.REQUEST)  # POST

    if accepts_html(request):
        return HttpResponse('success')
    elif accepts_xml(request):
        return xml_obj_response({'success': True})
    elif accepts_json(request):
        return json_obj_response({'success': True})
    else:
        return render(request, 'tasks/one_task.html', {'task': task})

@require_http_methods(['DELETE'])
def delete_task(request, task_id):
    try:
        Task.objects.get(id=task_id).delete()
    except ObjectDoesNotExist:
        # FIXME: change format.
        return HttpResponse('Does not exist.', status=500)

    if accepts_html(request):
        return HttpResponse('success')
    elif accepts_xml(request):
        return xml_obj_response({'success': True})
    elif accepts_json(request):
        return json_obj_response({'success': True})
    else:
        return HttpResponse('success')

# -- helpers --

def update_task_from_data(task, data):
    s = 'title'
    if s in data: setattr(task, s, data[s])
    s = 'details'
    if s in data: setattr(task, s, data[s])
    s = 'due_date'
    if s in data: setattr(task, s, date_from_str(data[s]))
    s = 'priority'
    if s in data: setattr(task, s, int(data[s]))
    s = 'is_completed'
    if s in data: setattr(task, s, data[s] == 'true')
    task.save()

def get_sort(req_data):
    sort_prefix = get_sort_prefix(req_data)
    sort_attr = get_sort_attr(req_data)
    return sort_prefix + sort_attr

def get_sort_attr(req_data):
    a = 'sort_attr'
    return req_data[a] if a in req_data else 'priority'

def get_sort_prefix(req_data):
    a = 'sort_is_asc'
    is_asc = req_data[a] == 'true' if a in req_data else False
    return '' if is_asc else '-'

def create_task_from_data(req_data):
    task = Task(title = req_data['title'],
                details = req_data['details'],
                due_date = get_due_date(req_data),
                is_completed = get_is_completed(req_data),
                priority = get_priority(req_data))
    task.save()
    return task

def date_from_str(s):
    try:
        return datetime.strptime(s, '%b %d, %Y').date()
    except ValueError:
        return datetime.strptime(s, '%B %d, %Y').date()

def get_due_date(req_data):
    if 'due_date' in req_data:
        return date_from_str(req_data['due_date'])
    else:
        return date.today()

def get_priority(req_data):
    if 'priority' in req_data:
        return int(req_data['priority'])
    else:
        return 2

def get_is_completed(req_data):
    if 'is_completed' in req_data:
        return req_data['is_completed'] == 'true'
    else:
        return False

def get_index_template(is_ajax):
    if is_ajax:
        return 'tasks/all_tasks.html'
    else:
        return 'tasks/index.html'

# -- unused --
def all_tasks_html(status=200, location=None):
    # how sorted?
    tasks = Task.objects.all()
    # template = loader.get_template('tasks/all_tasks.html')
    context = Context({
        'tasks': tasks,
        'priorities': Task.PRIORITIES
    })
    return make_response(
        template.render(context), 'text/html', status, location)

