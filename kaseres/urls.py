from django.conf.urls import patterns, url

from kaseres import views

urlpatterns = patterns(
    '',

    # On client...
    # When (re)displaying results, do we...
    #
    # 1. Request the entire (sorted) list and display it?
    # -OR-
    # 2. Update client data model and redisplay it?
    #

    # Should the path contain the verb?
    # Or is using the right verb enough info?

    # GET
    # home page: show all tasks
    # ex: /kaseres/
    #
    # Query string is in request.GET:
    #   * how sort
    #   * how many results
    #   * etc.
    url(r'^tasks/$', views.index, name='index'),

    # POST (create)
    # ex: /kaseres/create/
    url(r'^tasks/create/$', views.create_task, name='create_task'),

    # GET (read)
    # ex: /kaseres/12/read/
    url(r'^tasks/(?P<task_id>\d+)/read/', views.read_task, name='read_task'),

    # PUT (update) - idempotent w/ same params
    # ex: /kaseres/12/update/
    # Where do we pass in the k:v pairs?  PUT data?
    url(r'^tasks/(?P<task_id>\d+)/update/$', views.update_task, name='update_task'),

    # DELETE (delete)
    # ex: /kaseres/12/delete/
    url(r'^tasks/(?P<task_id>\d+)/delete/$', views.delete_task, name='delete_task'),
)
