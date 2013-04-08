
# Click on an item, and it becomes an editable version of itself.
# title, details, due_date -> text input

on_ajax_error = (jqXHR, textStatus, errorThrown) ->
    console.log textStatus
    console.log errorThrown
    console.log jqXHR

state =
    details_showing: false
    # after_create: false
    sort:
        column: 'priority'
        is_asc:
            title: true
            due_date: true
            priority: false
            is_completed: true

# -- sort --

display_sorted_tasks = (htmlStr, textStatus, jqXHR) ->
    $('#tasks_container').html(htmlStr)
    highlight_column state.sort.column
    init_delete_btns()
    init_details_display()
    init_datepicker()
    init_edit()

sort_tasks_by = (attr, is_asc) ->
    $.ajax
        url: '/kaseres/tasks/'
        type: 'GET'
        data:
            sort_attr: attr
            sort_is_asc: is_asc
        cache: false
        dataType: 'html'
        success: display_sorted_tasks
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
    attr = this.id.match(/^sort_(.+)$/)[1]
    set_sort_state attr
    set_sort_btn_imgs attr
    sort_tasks_by attr, state.sort.is_asc[attr]
    highlight_column attr

init_sort = ->
    $('.sort_btn').click click_sort_btn
    set_sort_btn_imgs state.sort.column
    highlight_column state.sort.column

# -- edit task --

init_datepicker = ->
    $('.date').datepicker {dateFormat: 'MM d, yy'}

show_saved = (evt) ->
    console.log 'saved!'

update_task = (task_id, attr, old_val, new_val) ->
    return unless new_val != old_val
    console.log "Saving task #{task_id}'s new #{attr}: #{new_val}"
    if state.sort.column == attr
        $("#task_#{attr}_#{task_id}").removeClass 'highlighted'
    data = {}
    data[attr] = new_val
    $.ajax
        type: 'POST' #'PUT'
        url: "/kaseres/tasks/#{task_id}/update/"
        data: data
        dataType: 'html'  # perhaps json, w/ sorting info?
        cache: false
        error: on_ajax_error
        success: show_saved

save_title = (evt) ->
    # Set html to new title.
    new_title = $.trim $(this).val()
    $("#task_title_#{evt.data.task_id}").html(new_title).click(edit_title)
    # Update the task as necessary.
    update_task evt.data.task_id, 'title', evt.data.prev_title, new_title

edit_title = ->
    # Remove onClick handler.
    $(this).unbind()
    # Get previous title (and task_id).
    task_id = this.id.match(/^task_title_(.+)$/)[1]
    prev_title = $.trim $(this).html()
    # Replace text with text-input.
    $(this).html "<input id='temp_edit' type='text' value='#{prev_title}' />"
    # Give it focus.  When it loses it, we're done.
    $('#temp_edit').
        focus().
        blur {task_id: task_id, prev_title: prev_title}, save_title

init_edit = ->
    $('.attr.title').click edit_title

# -- add task --

prepend_task = (htmlStr, textStatus, jqXHR) ->
    task_id = htmlStr.match(/^<li id=\"task_(\d+)\"/)[1]
    $('#tasks').prepend htmlStr

    # FIXME: No need to apply these handlers to ALL of them.  Just the new one.
    init_delete_btns()
    init_datepicker()
    init_edit()

    $("#task_details_#{task_id}").hide()
    $("#task_title_#{task_id}").click()

click_add_btn = ->
    # state.after_create = true
    $.ajax
        type: 'POST'
        url: '/kaseres/tasks/create/'
        data:
            sort_attr: state.sort.column
            sort_direction: state.sort.is_asc[state.sort.column]
            title: 'ADD TITLE'
            details: ''
        dataType: 'html'
        cache: false
        error: on_ajax_error
        success: prepend_task

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
    $('#toggle_details').click(click_toggle_details).hide()
    set_details_btn_text()
    init_details_display()

# -- init --

init_all = ->
    init_sort()
    init_toggle_details_btn()
    init_add_btn()
    init_delete_btns()
    init_datepicker()
    init_edit()

$(document).ready init_all
