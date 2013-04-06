
# -- sort --

bg_colors = {sort: 'LightSteelBlue', regular: 'White'}
sort_column = 'priority'

sort_by_attr = (attr_name) ->
        # make ajax call to index, w/ sort=attr_name
        1

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

# -- delete task --

delete_task = (id) ->
        # ajax

click_delete = (evt) ->
        return unless confirm 'Delete this task?'
        task_id = this.id.match(/^delete_(.*)$/)[1]
        elem = $ "#task_#{task_id}"
        elem.toggle 200, -> elem.remove()
        delete_task task_id

init_delete_btns = ->
        $('.delete_btn').click click_delete
        
# -- show/hide details --

details_showing = true

set_details_btn_text = ->
        verb = if details_showing then 'Hide' else 'Show'
        $('#toggle_details').html(verb + ' Details')

click_toggle_details = (evt) ->
        $('.task_details').toggle 200
        details_showing = not details_showing
        set_details_btn_text()

init_toggle_details_btn = ->
        $('#toggle_details').click click_toggle_details
        set_details_btn_text()

# -- init --

init_all = ->
        init_sort()
        init_toggle_details_btn()
        init_delete_btns()

$(document).ready init_all
