/**
 * Created by sliu on 5/18/16.
 */
$('.projectNodeNew #id_type').on('change', function(){
    var item_id = $(this).find('option:selected').val(),
        location = '#project-node-new-properties';
    load_keys_from_type_contents(item_id, location, 'node');
});

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
        edge_type = $('#project-edge-new-type option:selected').text(),
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

    $('#property-table tbody tr').each(function(){
        data += this.id + ' ';
    });
    $('input[name="property_data_index"]').val(data);
});

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

function load_keys_from_type_contents(item_id, location, type){
    $.getJSON("{% url 'graphs:get_keys_from_type' %}?id={0}&type={1}".format(item_id, type)).done(function(data){
        var keys = data['keys'],
            subkeys = data['subkeys'],
            rowCounter = 0,
            contents = '';
        $.each(keys, function(k, v){
            if ((keys[k].indexOf('Data') >= 0) || (keys[k] == 'Condition')) {
                contents += '<div class=\'row\' style=\'margin-top: 5px;\'>';
                contents += '<div class=\'col-xs-3\'><label>{0}: </label></div>'.format(keys[k]);
                contents += '</div>';

                contents += '<div class=\'row\' style=\'margin-top: 5px;\'>';
                contents += '<div class=\'col-xs-1\'></div>';
                contents += '<div class=\'col-xs-11\'>';
                contents += '<table class=\'table\' id=\'{0}-property-table\'>'.format(type);

                contents += '<thead><tr>';
                $.each(subkeys, function(k, v){
                    contents += '<th class=\'col-xs-2\'>{0}</th>'.format(subkeys[k]);
                });
                if (keys[k].indexOf('InputData') >= 0) {
                    contents += '<th class=\'col-xs-2\'><button id=\'buttonAddData\' class=\'btn btn-xs\' type=\'button\'>Add Data</button></th>';
                } else {
                    contents += '<th class=\'col-xs-2\'></th>';
                }
                contents += '</tr></thead>';

                contents += '<tbody>';

                contents += '<tr id=\'{0}\'>'.format(rowCounter);
                $.each(subkeys, function(k, v){
                    contents += '<td><input name=\'{0}_{1}\'/></td>'.format(subkeys[k], rowCounter);
                });
                contents += '</tr>';

                contents += '</tbody></table>';
                contents += '</div>';
                contents += '</div>';
            } else {
                contents += '<div class=\'row\' style=\'margin-top: 5px;\'>';
                contents += '<div class=\'col-xs-3\'><label>{0}: </label></div>'.format(keys[k]);
                contents += '<div class=\'col-xs-2\'><input name=\'{0}\'/></div>'.format(keys[k]);
                contents += '</div>';
            }
        });
        //console.log(contents)
        $(location).html(contents);

        $('#buttonAddData').click(function(){
            rowCounter++;
            node_property_add_data(subkeys, rowCounter);
        });
    });
}

function node_property_add_data(subkeys, rowCounter){
    var newRow = '';

    newRow += '<tr id=\'{0}\'>'.format(rowCounter);
    $.each(subkeys, function(k, v){
        newRow += '<td><input name=\'{0}_{1}\'/></td>'.format(subkeys[k], rowCounter);
    });
    newRow += '<td class=\'text-center\'><a href=\'#\' onclick=\'deleteRow(this);\'><i class=\'fa fa-trash-o fa-lg\'></i></a></td>';
    newRow += '</tr>';
    $('#node-property-table').append(newRow)
}

function deleteRow(row){
    $(row).closest('tr').remove();
}

$('.projectNodeNew').on('submit', function(){
    var data = '',
        location = '#projectNodeNewErrMessage',
        name = $('.projectNodeNew #id_name').val();

    if (name == ''){
        showErrMsg(location, 'Name is empty.');
        return false;
    }

    $('#property-table tbody tr').each(function(){
        data += this.id + ' ';
    });
    $('input[name="property_data_index"]').val(data);
});