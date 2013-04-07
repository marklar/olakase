
# Click on an item, and it becomes an editable version of itself.
# title, details, due_date -> text input

on_ajax_error = (jqXHR, textStatus, errorThrown) ->
    console.log textStatus
    console.log errorThrown
    console.log jqXHR

state =
    details_showing: false
    after_create: false
    sort:
        column: 'priority'
        is_asc:
            title: true
            due_date: true
            priority: false
            is_completed: true

# -- sort --

update_tasks = (htmlStr, textStatus, jqXHR) ->
    $('#tasks_container').html(htmlStr)
    highlight_column state.sort.column
    init_delete_btns()
    init_details_display()
    init_datepicker()

    if state.after_create
        state.after_create = false
        $('#tasks > li').filter(':first').toggle().toggle 200
        $('#tasks > li:first .attr').removeClass 'highlighted'
        #
        # TODO: set focus on title
        #

sort_tasks_by = (attr, is_asc) ->
    $.ajax
        url: '/kaseres/tasks/'
        type: 'GET'
        data:
            sort_attr: attr
            sort_is_asc: is_asc
        cache: false
        dataType: 'html'
        success: update_tasks
        error: -> on_ajax_error

set_sort_state = (attr) ->
    s = state.sort
    if s.column == attr
        s.is_asc[attr] = not s.is_asc[attr]
    else
        s.column = attr

set_sort_btn_imgs = (attr) ->
    $('.sort_arrow').hide()
    dir = if state.sort.is_asc[attr] then 'up' else 'dn'
    $("##{dir}_arrow_#{attr}").show()

highlight_column = (attr) ->
    $(".attr.#{attr}").addClass 'highlighted'

click_sort_btn = (evt) ->
    attr = this.id.match(/^sort_(.*)$/)[1]
    set_sort_state attr
    set_sort_btn_imgs attr
    sort_tasks_by attr, state.sort.is_asc[attr]
    highlight_column attr

init_sort = ->
    $('.sort_btn').click click_sort_btn
    set_sort_btn_imgs state.sort.column
    highlight_column state.sort.column

# -- edit task --

# 

# -- add task --

click_add_btn = ->
    state.after_create = true
    $.ajax
        type: 'POST'
        url: '/kaseres/tasks/create/'
        data:
            sort_attr: state.sort.column
            sort_direction: state.sort.direction[state.sort.column]
            title: 'ADD TITLE'
            details: ''
        dataType: 'html'
        cache: false
        error: on_ajax_error
        success: update_tasks

init_add_btn = ->
    $('#add_task').click click_add_btn

# -- delete task --

delete_task = (id) ->
    $.ajax
        type: 'DELETE'
        url: "/kaseres/tasks/#{id}/delete/"
        cache: false
        error: on_ajax_error
        success: -> console.log 'success!'

click_delete = (evt) ->
    return unless confirm 'Delete this task?'
    task_id = this.id.match(/^delete_(.*)$/)[1]
    elem = $ "#task_#{task_id}"
    elem.toggle 200, -> elem.remove()
    delete_task task_id

init_delete_btns = ->
    $('.delete_btn').click click_delete
        
# -- show/hide details --

set_details_btn_text = ->
    verb = if state.details_showing then 'Hide' else 'Show'
    $('#toggle_details').html(verb + ' Details')

click_toggle_details = (evt) ->
    $('.task_details').toggle 200
    state.details_showing = not state.details_showing
    set_details_btn_text()

init_details_display = ->
    $('.task_details').toggle() if not state.details_showing

init_toggle_details_btn = ->
    $('#toggle_details').click click_toggle_details
    set_details_btn_text()
    init_details_display()

# -- init --

init_datepicker = ->
    $('.date').datepicker {dateFormat: 'MM d, yy'}

init_all = ->
    init_sort()
    init_toggle_details_btn()
    init_add_btn()
    init_delete_btns()
    init_datepicker()

$(document).ready init_all
