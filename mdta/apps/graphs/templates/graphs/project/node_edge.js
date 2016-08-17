/**
 * Created by sliu on 5/18/16.
 */
$('.projectNodeNew #id_type').on('change', function(){
    var item_id = $(this).find('option:selected').val(),
        location = '#project-node-new-properties';
    load_keys_from_type_contents(item_id, location, 'node');
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
    var edge_type = $('#project-edge-new-type option:selected').text(),
        location = '#projectEdgeNewErrMessage',
        properties = $('#project-edge-new-properties input'),
        properties_no_input = true;

    $.each(properties, function(index){
        if (properties[index].value != ''){
            properties_no_input = false;
            return false;
        }
    });

    if (properties_no_input && edge_type != 'Connector'){
        showErrMsg(location, 'At lease input one property');
        return false;
    }
});

$(document).ready(function(){
    var node_id = $('.projectNodeNew #id_type').find('option:selected').val(),
        edge_id = $('.projectEdgeNew #project-edge-new-type').find('option:selected').val(),
        node_location = '#project-node-new-properties',
        edge_location = '#project-edge-new-properties';
    if (node_id) {
        load_keys_from_type_contents(node_id, node_location, 'node');
    }
    if (edge_id) {
        load_keys_from_type_contents(edge_id, edge_location, 'edge');
    }
});

function load_keys_from_type_contents(item_id, location, type){
    $.getJSON("{% url 'graphs:get_keys_from_type' %}?id={0}&type={1}".format(item_id, type)).done(function(data){
        var contents = '';
        $.each(data, function(k, v){
            contents += '<div class=\'col-xs-2\'><label>{0}: </label> <input name=\'{0}\'/></div>'.format(data[k]);
        });
        //console.log(contents)
        $(location).html(contents)
    })
}

function load_nodes_from_module(module_id, location){
    $.getJSON("{% url 'graphs:get_nodes_from_module' %}?module_id={0}".format(module_id)).done(function(data){
        var option = '';
        $.each(data, function(k, v){
            option += '<option value={0}>{1}</option>'.format(v['id'], v['name']);
        });
        $(location).empty().append(option);
    });
}