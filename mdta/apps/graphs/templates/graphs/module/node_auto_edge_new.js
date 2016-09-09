/* Start Module Node New Node & Edge Code */
$(document).ready( function(){
    var node_type_id = $('.moduleNodeEdgeNew #id_type').find('option:selected').val(),
        node_location = '#module-node-edge-new-node-properties',
        edge_type_id = $('.moduleNodeEdgeNew #id_edge_type').find('option:selected').val(),
        edge_location = '#module-node-edge-new-edge-properties';

    load_keys_from_type_contents(node_type_id, node_location, 'node');
    load_keys_from_type_contents(edge_type_id, edge_location, 'edge');
});

$('.moduleNodeEdgeNew #id_type').on('change', function(){
    var node_type_id = $(this).find('option:selected').val(),
        location = '#module-node-edge-new-node-properties';

    load_keys_from_type_contents(node_type_id, location, 'node');
});

$('.moduleNodeEdgeNew #id_edge_type').on('change', function(){
    var edge_type_id = $(this).find('option:selected').val(),
        location = '#module-node-edge-new-edge-properties';

    load_keys_from_type_contents(edge_type_id, location, 'edge');
});

$('.moduleNodeEdgeNew form').on('submit', function(e){
    var node_name = $('.moduleNodeEdgeNew #id_name').val(),
        err_location = '#moduleNodeEdgeNewErrMessage',
        edge_type = $('#moduleNodeEdgeNewEdgeType option:selected').text(),
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
