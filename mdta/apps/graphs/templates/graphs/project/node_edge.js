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
        name = $('.projectNodeNew #id_name').val();

    if (name == ''){
        showErrMsg(location, 'Name is empty.');
        return false;
    }

    $('#node-property-table tbody tr').each(function(){
        data += this.id + ' ';
    });
    $('input[name="property_data_index"]').val(data);
});

/* ---------------End Project/Module Node New ---------------*/

/* ---------------Start Project/Module Edge New ---------------*/
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
        edge_type_project = $('#project-edge-new-type option:selected').text(),
        edge_type_module = $('#id_type option:selected').text(),
        location = '#projectEdgeNewErrMessage',
        properties = $('#project-edge-new-properties input'),
        properties_no_input = true;

    $.each(properties, function(index){
        if (properties[index].value != ''){
            properties_no_input = false;
            return false;
        }
    });

    if ((properties_no_input && edge_type_project != 'Connector') && edge_type_project) {
        showErrMsg(location, 'Please Input property');
        return false;
    }

    if ((properties_no_input && edge_type_module != 'Connector') && edge_type_module) {
        showErrMsg(location, 'Please Input property');
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
    } else if (edge_id_project) {
        load_keys_from_type_contents(edge_id_project, edge_location, 'edge');
    } else if (edge_id_module) {
        load_keys_from_type_contents(edge_id_module, edge_location, 'edge');
    }
});


function load_nodes_from_module(module_id, location){
    $.getJSON("{% url 'graphs:get_nodes_from_module' %}?module_id={0}".format(module_id)).done(function(data){
        var option = '';
        $.each(data, function(k, v){
            option += '<option value={0}>{1}</option>'.format(v['id'], v['name']);
        });
        $(location).empty().append(option);
    });
}


