/**
 * Created by sliu on 6/8/16.
 */



/* Start Module Node Edit Code */
$('.moduleNodeEditForm #moduleNodeEditType').on('change', function(e){
    var type_id = $(this).find('option:selected').val(),
        location = $(this).closest('.moduleNodeEditForm').find('#module-node-edit-properties');

    load_keys_from_type_contents(type_id, location, 'node', 'module_node_edit');
});

$('.moduleNodeEditForm').on('submit', function(e){
    var name = $(e.currentTarget).find('input[name="moduleNodeEditName"]').val(),
        location = $(e.currentTarget).find('#moduleNodeEditErrMessage'),
        properties = $(e.currentTarget).find('#module-node-edit-properties input'),
        is_json_format = true,
        json_msg = '',
        data = '';

    if (name == ''){
        showErrMsg(location, 'Name is Empty');
        return false;
    }

    var check_json = check_node_properties_json(properties);


    if (!check_json['is_json_format']) {
        showErrMsg(location, check_json['json_msg']);
        return false;
    }

    $(e.currentTarget).find('.moduleNodeEditPropertyTable tbody tr').each(function(){
        data += this.id + ' ';
    });
    $(e.currentTarget).find('input[name="property_data_index"]').val(data);

});

function check_node_properties_json(properties){
    var data = {},
        item = '',
        item_str = '',
        json_msg = '',
        is_json_format = true;

    $.each(properties, function(index){
        item = properties[index];
        if (item.name.indexOf('Inputs_') >= 0 || item.name.indexOf('Outputs_') >= 0) {
            item_str = item.value.replace(/'/g, '"');
            if (!isJsonFormat(item_str)){
                if (item_str.length > 0){
                    json_msg = 'JSON format incorrect: {0}'.format(item.name);
                } else {
                    json_msg = 'JSON input empty: {0}'.format(item.name);
                }
                is_json_format = false;
                return false;
            }
        }
    });

    data['is_json_format'] = is_json_format;
    data['json_msg'] = json_msg;

    return data;
}
/* End Module Node Edit Code */


/* Start Module Edge Edit Code */
$('.moduleEdgeEditForm #moduleEdgeEditType').on('change', function(){
    var edge_type_id = $(this).find('option:selected').val(),
        location = $(this).closest('.moduleEdgeEditForm').find('#module-edge-edit-properties');

    load_keys_from_type_contents(edge_type_id, location, 'edge');
});

$('.moduleEdgeEditForm').on('submit', function(e){
    var location = $(e.currentTarget).find('#moduleEdgeEditErrMessage'),
        properties = $(e.currentTarget).find('#module-edge-edit-properties input'),
        //edge_type = $(e.currentTarget).find('#moduleEdgeEditType option:selected').text(),
        submit = $(e.currentTarget).find('button[type="submit"]:focus');

    //console.log(edge_type)

    var check_json = check_edge_properties_json(properties);

    //if (check_json['properties_no_input'] && edge_type != 'Connector' && submit[0].textContent == 'Save'){
    //    showErrMsg(location, 'Input of property empty');
    //    return false;
    //}

    if (!check_json['is_json_format']){
        showErrMsg(location, check_json['json_msg']);
        return false;
    }
});

function check_edge_properties_json(properties){
    var data = {},
        item = '',
        item_str = '',
        json_msg = '',
        is_json_format = true;

    $.each(properties, function(index){
        item = properties[index];
        if (item.name.indexOf('Outputs_') >= 0 || item.name.indexOf('Condition_') >= 0) {
            item_str = properties[index].value.replace(/'/g, '"');
            if (!isJsonFormat(item_str)){
                if (item_str.length > 0){
                    json_msg = 'JSON format incorrect: {0}'.format(item.name);
                } else {
                    json_msg = 'JSON input empty: {0}'.format(item.name);
                }
                is_json_format = false;
                return false;
            }
        }
    });

    data['is_json_format'] = is_json_format;
    data['json_msg'] = json_msg;

    return data;
}

function isJsonFormat(str){
    var is_json = true;
    try {
        var json = $.parseJSON(str);
    } catch(e){
        is_json = false
    }
    return is_json
}
/* End Module Edge Edit Code */


$(document).ready(function(){
    draw_module_graph();
    autocomplete_nodename_and_edgekeys();
});

function draw_module_graph(){
    var container = document.getElementById('node_in_module');

    // provide the data in the vis format
    var data = {
        nodes: nodes,
        edges: edges
    };
    var options = {
        nodes: {
            shape: 'box',
            font: {
                size: 14, //px
            }
        },
        edges: {
            //style: 'arrow',
            color: '#000',
            length: 190,
            arrows: 'to'
        },
        width: '100%',
        height: '800px',
        physics: {
            barnesHut: {
                gravitationalConstant: -4000
            }
        }
    };

    // initialize your network!
    var network = new vis.Network(container, data, options);

    network.on('click', function(params){
        //console.log(params.nodes)
        if (!$.isEmptyObject(params.nodes)) {
            $('a[href="#moduleNodeEdit"]').click();
            $('a[href="#node-{0}"]'.format(params.nodes)).click();
        } else if (!$.isEmptyObject(params.edges)) {
            $('a[href="#moduleEdgeEdit"]').click();
            $('a[href="#edge-{0}"]'.format(params.edges)).click();
        } else {
            $('a[href="#moduleNodeEdgeEmpty"]').click();
        }
    });

    network.on('doubleClick', function(params){
        if (!$.isEmptyObject(params.nodes)){
            $.getJSON("{% url 'graphs:get_module_id_from_node_id' %}?node_id={0}".format(params.nodes)).done(function(data){
                //console.log(data);
                var base_url = '',
                    tmp = window.location.href.split('/'),
                    current_module_id = tmp[tmp.length - 2];

                for (var i = 0; i < tmp.length - 2; i++) {
                    base_url += tmp[i] + '/'
                }
                if (!( data['module_id'] == current_module_id)){
                    window.location.href = base_url + data['module_id'];
                     $('body').css('cursor', 'progress');
                }
            })
        }
    })

}


/* Start Node Name for OnFailGoTo of MenuPrompt Code */

function autocomplete_nodename_and_edgekeys(call_from) {
    var myToggle = $('.myToggle'),
        project_node_new = $('.projectNodeNew input[name="OnFailGoTo"]'),
        module_node_edit = $('.moduleNodeEditForm input[name="OnFailGoTo"]'),
        data_edge_keys = $('.data_edge_keys'),
        node_edge_new = $('.moduleNodeEdgeNew input[name="node_OnFailGoTo"]'),
        input_element = $('input[name="Outputs_0"]'),
        input_edge_element = $('input[name="edge_Outputs_0"]');

    switch (call_from){
        case 'node':
            myToggle.bootstrapToggle();
            project_node_new.autocomplete({
                source: node_names_autocomplete
            });
            module_node_edit.autocomplete({
                source: node_names_autocomplete
            });
            data_edge_keys.autocomplete({
                source: data_edge_keys_autocomplete,
                select: function (event, ui) {
                    var str = '{\'{0}\': \' \'}'.format(ui.item.value);
                    input_element.val(str);
                }
            });
            break;
        case 'auto_node':
            myToggle.bootstrapToggle();
            node_edge_new.autocomplete({
                source: node_names_autocomplete
            });
            break;
        case 'edge':
            myToggle.bootstrapToggle();
            data_edge_keys.autocomplete({
                source: data_edge_keys_autocomplete,
                select: function (event, ui) {
                    var str = '{\'{0}\': \' \'}'.format(ui.item.value);
                    input_element.val(str);
                }
            });
            break;
        case 'auto_edge':
            myToggle.bootstrapToggle();
            data_edge_keys.autocomplete({
                source: data_edge_keys_autocomplete,
                select: function (event, ui) {
                    var str = '{\'{0}\': \' \'}'.format(ui.item.value);
                    input_edge_element.val(str);
                }
            });
            break;
        default:
            project_node_new.autocomplete({
                source: node_names_autocomplete
            });

            module_node_edit.autocomplete({
                source: node_names_autocomplete
            });

            data_edge_keys.autocomplete({
                source: data_edge_keys_autocomplete,
                select: function (event, ui) {
                    var str = '{\'{0}\': \' \'}'.format(ui.item.value);
                    input_element.val(str);
                }
            });
    }
}


/* End   Node Name for OnFailGoTo of MenuPrompt Code */