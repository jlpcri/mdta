/**
 * Created by sliu on 5/18/16.
 */

/* ---------------Start Project/Module Node New ---------------*/
$('.projectNodeNew #id_type').on('change', function(){
    var item_id = $(this).find('option:selected').val(),
        location = '#project-node-new-properties';
    load_keys_from_type_contents(item_id, location, 'node');
});

$('.projectNodeNew').on('submit', function(){
    var data = '',
        location = '#projectNodeNewErrMessage',
        name = $('.projectNodeNew #id_name').val(),
        properties = $('#project-node-new-properties input');

    if (name == ''){
        showErrMsg(location, 'Name is empty.');
        return false;
    }

    $('#node-property-table tbody tr').each(function(){
        data += this.id + ' ';
    });
    $('input[name="property_data_index"]').val(data);

    var check_json = check_node_properties_json(properties);
    if (!check_json['is_json_format']) {
        showErrMsg(location, check_json['json_msg']);
        return false;
    }
});

/* ---------------End Project/Module Node New ---------------*/

/* ---------------Start Project/Module Edge New ---------------*/
// $('#module-edge-new-modal').on('shown.bs.modal', function(){
//     var node_id = $('#select_node_id').val();
//     if (node_id > 1){
//         $('#project-edge-new-from-node').val(node_id)
//     } else {
//         $('#project-edge-new-from-node').val($('#project-edge-new-to-node').val())
//     }
// });

$('.projectEdgeNew #id_type').on('change', function(){
    var item_id = $(this).find('option:selected').val(),
        location = '#project-edge-new-properties';
    load_keys_from_type_contents(item_id, location, 'edge');
});

$('.projectEdgeNew #project-edge-new-type').on('change', function(){
    var item_id = $(this).find('option:selected').val(),
        location = '#project-edge-new-properties';
    load_keys_from_type_contents(item_id, location, 'edge');
});

$('.projectEdgeNew #project-edge-new-from-module').on('change', function(){
    var module_id = $(this).find('option:selected').val(),
        location = '#project-edge-new-from-node';

    load_nodes_from_module(module_id, location);
});

$('.projectEdgeNew #project-edge-new-to-module').on('change', function(){
    var module_id = $(this).find('option:selected').val(),
        location = '#project-edge-new-to-node';

    load_nodes_from_module(module_id, location);
});

$('.projectEdgeNew').on('submit', function(){
    var data = '',
        from_node = $('#project-edge-new-from-node option:selected').text(),
        to_node = $('#project-edge-new-to-node option:selected').text(),
        location = '#projectEdgeNewErrMessage',
        properties = $('#project-edge-new-properties input');

    var check_json = check_edge_properties_json(properties);

    if (from_node == ''){
        showErrMsg(location, 'From Node empty');
        return false;
    } else if (to_node == ''){
        showErrMsg(location, 'To Node empty');
        return false;
    }

    if (!check_json['is_json_format']){
        showErrMsg(location, check_json['json_msg']);
        return false;
    }

    $('#edge-property-table tbody tr').each(function(){
        data += this.id + ' ';
    });
    $('input[name="property_data_index"]').val(data);
});

/* ---------------End Project/Module Edge New ---------------*/

$(document).ready(function(){
    var node_id = $('.projectNodeNew #id_type').find('option:selected').val(),
        edge_id_project = $('.projectEdgeNew #project-edge-new-type').find('option:selected').val(),
        edge_id_module = $('.projectEdgeNew #id_type').find('option:selected').val(),
        node_location = '#project-node-new-properties',
        edge_location = '#project-edge-new-properties';
    if (node_id) {
        load_keys_from_type_contents(node_id, node_location, 'node');
    }
    if (edge_id_project) {
        load_keys_from_type_contents(edge_id_project, edge_location, 'edge');
    } else if (edge_id_module) {
        load_keys_from_type_contents(edge_id_module, edge_location, 'edge');
    }
});


function load_nodes_from_module(module_id, location, node_id){
    $.getJSON("{% url 'graphs:get_nodes_from_module' %}?module_id={0}".format(module_id)).done(function(data){
        var option = '';
        $.each(data, function(k, v){
            if (v['id'] == node_id){
                option += '<option value={0} selected>{1}</option>'.format(v['id'], v['name']);
            } else {
                option += '<option value={0}>{1}</option>'.format(v['id'], v['name']);
            }
        });
        $(location).empty().append(option);
    });
}


