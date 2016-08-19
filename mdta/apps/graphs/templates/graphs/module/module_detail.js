/**
 * Created by sliu on 6/8/16.
 */

/* Start Module Node New Code */
$('.moduleNodeNew').on('show.bs.modal', function(){
    var node_type_id = $('.moduleNodeNew #id_type').find('option:selected').val(),
        node_properties_location = '#module-node-new-properties';

    load_keys_from_node_edge_type(node_type_id, node_properties_location, 'node');
});

$('.moduleNodeNew form').on('submit', function(){
    var name = $('.moduleNodeNew #id_name').val();
    if (name == ''){
        showErrMsg('#moduleNodeNewErrMessage', 'Name is Empty.');
        return false;
    }
});

$('.moduleNodeNew #id_type').on('change', function(){
    var type_id = $(this).find('option:selected').val(),
        location = '#module-node-new-properties';
    load_keys_from_node_edge_type(type_id, location, 'node');
});
/* End Module Node New Code */

/* Start Module Node Edit Code */
$('.moduleNodeEditForm #moduleNodeEditType').on('change', function(e){
    var type_id = $(this).find('option:selected').val(),
        location = $(this).closest('.moduleNodeEditForm').find('#module-node-edit-properties');

    load_keys_from_node_edge_type(type_id, location, 'node');
});

$('.moduleNodeEditForm').on('submit', function(e){
    var name = $(e.currentTarget).find('input[name="moduleNodeEditName"]').val(),
        location = $(e.currentTarget).find('#moduleNodeEditErrMessage');

    if (name == ''){
        showErrMsg(location, 'Name is Empty');
        return false;
    }
});
/* End Module Node Edit Code */


/* Start Module Edge New Code */
$('.moduleEdgeNew').on('show.bs.modal', function(){
    var edge_type_id = $('.moduleEdgeNew #id_type').find('option:selected').val(),
        edge_properties_location = '#module-edge-new-properties';

    load_keys_from_node_edge_type(edge_type_id, edge_properties_location, 'edge');
});

$('.moduleEdgeNew form').on('submit', function(){
    var edge_type = $(this).find('#id_type option:selected').text().split(':')[0],
        location = '#moduleEdgeNewErrMessage',
        properties = $(this).find('#module-edge-new-properties input'),
        properties_no_input = true;

    //console.log(edge_type)
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

$('.moduleEdgeNew #id_type').on('change', function(){
    var edge_type_id = $(this).find('option:selected').val(),
        location = '#module-edge-new-properties';

    load_keys_from_node_edge_type(edge_type_id, location, 'edge');
});
/* End Module Edge New Code */

/* Start Module Edge Edit Code */
$('.moduleEdgeEditForm #moduleEdgeEditType').on('change', function(){
    var edge_type_id = $(this).find('option:selected').val(),
        location = $(this).closest('.moduleEdgeEditForm').find('#module-edge-edit-properties');

    load_keys_from_node_edge_type(edge_type_id, location, 'edge');
});

$('.moduleEdgeEditForm').on('submit', function(e){
    var edge_type = $(e.currentTarget).find('#moduleEdgeEditType option:selected').text(),
        location = $(e.currentTarget).find('#moduleEdgeEditErrMessage'),
        properties = $(e.currentTarget).find('#module-edge-edit-properties input'),
        properties_no_input = true,
        submit = $(e.currentTarget).find('button[type="submit"]:focus');

    //console.log(edge_type)

    $.each(properties, function(index){
        //console.log(index, properties[index].value);
        if (properties[index].value != ''){
            properties_no_input = false;
            return false;
        }
    });

    if (properties_no_input && edge_type != 'Connector' && submit[0].textContent == 'Save'){
        showErrMsg(location, 'At lease input one property');
        return false;
    }
});
/* End Module Edge Edit Code */

/* Start Module Node New Node & Edge Code */
$('.moduleNodeEdgeNew').on('show.bs.modal', function(e){
    var from_node_id = $(e.relatedTarget).data('from-node-id'),
        node_type_id = $('.moduleNodeEdgeNew #id_type').find('option:selected').val(),
        node_location = '#module-node-edge-new-node-properties',
        edge_type_id = $('.moduleNodeEdgeNew #moduleNodeEdgeNewEdgeType').find('option:selected').val(),
        edge_location = '#module-node-edge-new-edge-properties';

    $(e.currentTarget).find('input[name="moduleNodeEdgeNewFromNodeId"]').val(from_node_id);
    load_keys_from_node_edge_type_together(node_type_id, node_location, 'node');
    load_keys_from_node_edge_type_together(edge_type_id, edge_location, 'edge');
});

$('.moduleNodeEdgeNew #id_type').on('change', function(){
    var node_type_id = $(this).find('option:selected').val(),
        location = '#module-node-edge-new-node-properties';

    load_keys_from_node_edge_type_together(node_type_id, location, 'node');
});

$('.moduleNodeEdgeNew #moduleNodeEdgeNewEdgeType').on('change', function(){
    var edge_type_id = $(this).find('option:selected').val(),
        location = '#module-node-edge-new-edge-properties';

    load_keys_from_node_edge_type_together(edge_type_id, location, 'edge');
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


$(document).ready(function(){
    draw_module_graph();
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
        height: '800px'
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
        }
    })

}