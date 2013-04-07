
# Click on an item, and it becomes an editable version of itself.
# title, details, due_date -> text input

# -- sort --

bg_colors =
        sort: 'LightSteelBlue'
        regular: 'White'  # placeholder

# asc ('').  desc ('-').
sort_state =
        column: 'priority'
        direction:
                title: ''
                due_date: '-'
                priority: '-'
                is_completed: ''

update_tasks = (htmlStr, textStatus, jqXHR) ->
        # If this is called after 'create',
        # we should animate the appearance of the first task in the list,
        # and we should change its bg_color to show that it's out of sort order.
        $('#tasks_container').html(htmlStr)
        highlight_col sort_state.column
        init_delete_btns()
        init_details_display()
        init_datepicker()

sort_tasks_by = (attr, direction) ->
        # TODO: set sort
        $.ajax
                url: '/kaseres/tasks/'
                type: 'GET'
                data:
                        sort_attr: attr
                        sort_direction: direction
                cache: false
                dataType: 'html'
                success: update_tasks
                error: -> on_error

high_els = (els) -> els.css 'background-color', bg_colors.sort
low_els  = (els) -> els.css 'background-color', bg_colors.regular

highlight_col = (attr) ->
        high_els $(".attr.#{attr}")

unhighlight_col = (attr) ->
        low_els $(".attr.#{attr}")

unhighlight_task = (id) ->
        low_els $("##{id} .#{sort_state.column}")

toggle_sort_dir = (attr) ->
        sort_state.direction[attr] =
                if sort_state.direction[attr] == '-' then '' else '-'

set_sort_state = (attr) ->
        if sort_state.column == attr
                toggle_sort_dir attr
        else
                sort_state.column = attr

click_sort_btn = (evt) ->
        attr = this.id.match(/^sort_(.*)$/)[1]
        set_sort_state attr
        sort_tasks_by attr, sort_state.direction[attr]
        highlight_col attr

init_sort_btns = ->
        $('.sort_btn').click click_sort_btn

init_sort = ->
        init_sort_btns()
        bg_colors.regular = $('.attr').css 'background-color'
        highlight_col sort_state.column

# -- add task --

click_submit = ->
        $.ajax
                type: 'POST'
                url: '/kaseres/tasks/create/'
                data:
                        sort_attr: sort_state.column
                        sort_direction: sort_state.direction[sort_state.column]
                        title: 'bobo'
                        details: 'jungle'
                        due_date: 'February 1, 2013'
                        priority: 2
                        is_completed: true
                dataType: 'html'
                cache: false
                error: on_error
                success: update_tasks

click_add_btn = ->
        alert 'Open form for creating task.'
        click_submit()

init_add_btn = ->
        $('#add_task').click click_add_btn

# -- delete task --

on_error = (jqXHR, textStatus, errorThrown) ->
        console.log textStatus
        console.log errorThrown
        console.log jqXHR

delete_task = (id) ->
        $.ajax
            type: 'DELETE'
            url: "/kaseres/tasks/#{id}/delete/"
            cache: false
            error: on_error
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

details_showing = false

set_details_btn_text = ->
        verb = if details_showing then 'Hide' else 'Show'
        $('#toggle_details').html(verb + ' Details')

click_toggle_details = (evt) ->
        $('.task_details').toggle 200
        details_showing = not details_showing
        set_details_btn_text()

init_details_display = ->
        $('.task_details').toggle() if not details_showing

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
