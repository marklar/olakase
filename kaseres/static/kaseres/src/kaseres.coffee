
# Click on an item, and it becomes an editable version of itself.
# title, details, due_date -> text input

# -- sort --

bg_colors = {sort: 'LightSteelBlue', regular: 'White'}
sort_column = 'priority'

update_tasks = (htmlStr, textStatus, jqXHR) ->
        $('#tasks_container').html(htmlStr)
        highlight_col sort_column
        init_delete_btns()
        init_details_display()
        init_datepicker()

sort_by_attr = (attr_name) ->
        # TODO: set sort
        $.ajax
                url: '/kaseres/tasks/'
                type: 'GET'
                data: {attr: attr_name}
                cache: false
                dataType: 'html'
                success: update_tasks
                error: -> on_error

high_els = (els) -> els.css 'background-color', bg_colors.sort
low_els  = (els) -> els.css 'background-color', bg_colors.regular

highlight_col = (attr_name) ->
        high_els $(".attr.#{attr_name}")
        $("#sort_#{attr_name}").prop 'disabled', true

unhighlight_col = (attr_name) ->
        low_els $(".attr.#{attr_name}")

unhighlight_task = (id) ->
        low_els $("##{id} .#{sort_column}")

sort_by = (attr_name) ->
        sort_by_attr attr_name
        highlight_col attr_name
        sort_column = attr_name

click_sort_btn = (evt) ->
        $('.sort_btn').prop 'disabled', false
        unhighlight_col sort_column
        attr_name = this.id.match(/^sort_(.*)$/)[1]
        sort_by attr_name

init_sort_btns = ->
        $('.sort_btn').click click_sort_btn

init_sort = ->
        init_sort_btns()
        bg_colors.regular = $('.attr').css 'background-color'
        highlight_col sort_column

# -- add task --

submit_success = (htmlStr, textStatus, jqXHR) ->
        console.log 'success.  now add the DOM elements.'
        console.log htmlStr

click_submit = ->
        $.ajax
                type: 'POST'
                url: '/kaseres/tasks/create/'
                data:
                        title: 'my title'
                        details: 'my details'
                        due_date: new Date()
                        priority: 2
                dataType: 'html'
                cache: false
                error: on_error
                success: submit_success

click_add_btn = ->
        alert 'Open form for creating task.'
        click_submit()

init_add_btn = ->
        $('#add_task').click click_add_btn

# -- delete task --

on_error = (jqXHR, textStatus, errorThrown) ->
        console.log errorThrown

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
