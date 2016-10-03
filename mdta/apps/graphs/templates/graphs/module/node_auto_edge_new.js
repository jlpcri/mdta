/* Start Module Node New Node & Edge Code */
function load_keys_from_type_contents_edge(item_id, location, type){
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
                contents += '<th class=\'col-xs-2\'></th>';
                contents += '</tr></thead>';

                contents += '<tbody>';

                contents += '<tr id=\'{0}\'>'.format(rowCounter);
                $.each(subkeys, function(k, v){
                    contents += '<td><input name=\'{0}_{1}\' style=\'width:100%\' placeholder=\'JSON Format\'/></td>'.format(subkeys[k], rowCounter);
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
    });
}

$(document).ready( function(){
    var node_type_id = $('.moduleNodeEdgeNew #id_type').find('option:selected').val(),
        node_location = '#module-node-edge-new-node-properties',
        edge_type_id = $('.moduleNodeEdgeNew #id_edge-type').find('option:selected').val(),
        edge_location = '#module-node-edge-new-edge-properties';

    load_keys_from_type_contents(node_type_id, node_location, 'node');
    load_keys_from_type_contents_edge(edge_type_id, edge_location, 'edge');
});

$('.moduleNodeEdgeNew #id_type').on('change', function(){
    var node_type_id = $(this).find('option:selected').val(),
        location = '#module-node-edge-new-node-properties';

    load_keys_from_type_contents(node_type_id, location, 'node');
});

$('.moduleNodeEdgeNew #id_edge-type').on('change', function(){
    var edge_type_id = $(this).find('option:selected').val(),
        location = '#module-node-edge-new-edge-properties';

    load_keys_from_type_contents_edge(edge_type_id, location, 'edge');
});

$('.moduleNodeEdgeNew').on('submit', function(e){
    var node_name = $('.moduleNodeEdgeNew #id_name').val(),
        err_location = '#moduleNodeEdgeNewErrMessage',
        edge_type = $('.moduleNodeEdgeNew #id_edge-type option:selected').text(),
        edge_properties = $(e.currentTarget).find('#module-node-edge-new-edge-properties input'),
        edge_properties_no_input = true;

    if (node_name == ''){
        showErrMsg(err_location, 'Node Name is empty.');
        return false;
    }

    $.each(edge_properties, function(index){
        if (edge_properties[index].value != ''){
            edge_properties_no_input = false;
            return false;
        }
    });
    if (edge_properties_no_input && edge_type != 'Connector'){
        showErrMsg(err_location, 'At least input on edge property');
        return false;
    }
});

/* End Module Node New Node & Edge Code */
