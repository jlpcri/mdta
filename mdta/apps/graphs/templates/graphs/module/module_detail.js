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
$('.moduleNodeEdit').on('show.bs.modal', function(e){
    var node_id = $(e.relatedTarget).data('node-id'),
        node_type_id = $(e.relatedTarget).data('node-type-id'),
        node_name = $(e.relatedTarget).data('node-name'),
        node_properties = $(e.relatedTarget).data('node-properties'),
        node_properties_location = '#module-node-edit-properties';

    $(e.currentTarget).find('input[name="moduleNodeEditId"]').val(node_id);
    $(e.currentTarget).find('select').val(node_type_id);
    $(e.currentTarget).find('input[name="moduleNodeEditName"]').val(node_name);
    $('.moduleNodeEdit .modal-title').html('Node Edit/Delete');

    //load_keys_from_node_edge_type(node_type_id, node_properties_location, 'node');
    if (node_properties != 'None') {
        show_properties_for_node_edit(node_properties, node_properties_location);
    }
});

$('.moduleNodeEdit #moduleNodeEditType').on('change', function(){
    var type_id = $(this).find('option:selected').val(),
        location = '#module-node-edit-properties';

    load_keys_from_node_edge_type(type_id, location, 'node');
});

$('.moduleNodeEdit form').on('submit', function(){
    var name = $('#moduleNodeEditName').val();

    if (name == ''){
        showErrMsg('#moduleNodeEditErrMessage', 'Name is Empty');
        return false;
    }
});
/* End Module Node Edit Code */

/* Start Module Node Detail Code */
$('.moduleNodeDetail').on('show.bs.modal', function(e){
    var node_id = $(e.relatedTarget).data('node-id'),
        contents_head = '<tr><th>Name</th><th>Priority</th><th>ToNode</th>',
        contents_body = '',
        contents = '';

    // node_id passed from href link
    if (node_id) {
        $('.moduleNodeDetail').find('input[name="moduleNodeDetailId"]').val(node_id);
    }  // else passed from graph

    node_id = $('.moduleNodeDetail').find('input[name="moduleNodeDetailId"]').val();

    $.getJSON("{% url 'graphs:get_leaving_edges_from_node'%}?id={0}".format(node_id)).done(function(data){
        $.ajax({cache: false});
        if (data['edges'].length > 0) {
            $.each(data['edges'], function (index, value) {
                contents_body += '<tr><td>' + value['name'] + '</td><td>' + value['priority'] + '</td><td>' + value['to_node'] + '</td></tr>';
            });
            contents = "<table id='tableData' class='table table-bordered'>"
                + "<thead>" + contents_head + "</thead>"
                + "<tbody>" + contents_body + "</tbody>"
                + "</table>";
        } else {
            contents = '&nbsp;&nbsp;No leaving edges';
        }

        $('.moduleNodeDetail .modal-title').html('Node Detail - {0}'.format(data['node_name']));
        $('.moduleNodeDetail .modal-body .moduleNodeEdges').html(contents);
    });

});
/* End Module Node Detail Code */

/* Start Module Edge New Code */
$('.moduleEdgeNew').on('show.bs.modal', function(){
    var edge_type_id = $('.moduleEdgeNew #id_type').find('option:selected').val(),
        edge_properties_location = '#module-edge-new-properties';

    load_keys_from_node_edge_type(edge_type_id, edge_properties_location, 'edge');
});

$('.moduleEdgeNew form').on('submit', function(){
    var name = $('.moduleEdgeNew #id_name').val();
    if (name == ''){
        showErrMsg('#moduleEdgeNewErrMessage', 'Name is Empty.');
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
$('.moduleEdgeEdit').on('show.bs.modal', function(e){
    var edge_id = $(e.relatedTarget).data('edge-id'),
        edge_type_id = $(e.relatedTarget).data('edge-type-id'),
        edge_name = $(e.relatedTarget).data('edge-name'),
        edge_from = $(e.relatedTarget).data('edge-from'),
        edge_to = $(e.relatedTarget).data('edge-to'),
        edge_priority = $(e.relatedTarget).data('edge-priority'),
        edge_properties = $(e.relatedTarget).data('edge-properties'),
        edge_properties_location = '#module-edge-edit-properties';

    $(e.currentTarget).find('input[name="moduleEdgeEditId"]').val(edge_id);
    $(e.currentTarget).find('input[name="moduleEdgeEditName"]').val(edge_name);
    $(e.currentTarget).find('select[name="moduleEdgeEditType"]').val(edge_type_id);
    $(e.currentTarget).find('select[name="moduleEdgeEditFromNode"]').val(edge_from);
    $(e.currentTarget).find('select[name="moduleEdgeEditToNode"]').val(edge_to);
    $(e.currentTarget).find('select[name="moduleEdgeEditPriority"]').val(edge_priority);

    if (! $.isEmptyObject(edge_properties) && edge_properties != 'None'){
        show_properties_for_node_edit(edge_properties, edge_properties_location);
    }
});

$('.moduleEdgeEdit #moduleEdgeEditType').on('change', function(){
    var edge_type_id = $(this).find('option:selected').val(),
        location = '#module-edge-edit-properties';

    load_keys_from_node_edge_type(edge_type_id, location, 'edge');
});
/* End Module Edge Edit Code */

function load_keys_from_node_edge_type(item_id, location, type){
    $.getJSON("{% url 'graphs:get_keys_from_type' %}?id={0}&type={1}".format(item_id, type)).done(function(data){
        var contents = '';
        $.each(data, function(k, v){
            contents += '<div class=\'row\' style=\'margin-top: 10px;\'>';
			contents += '<div class=\'col-xs-1\'></div>';
			contents += '<div class=\'col-xs-4\'><label>{0}: </label></div>'.format(data[k]);
			contents += '<div class=\'col-xs-7\'><input name=\'{0}\'/></div>'.format(data[k]);
			contents += '</div>';
        });
        //console.log(contents)
        $(location).html(contents)
    })
}

function show_properties_for_node_edit(properties, location){
    //console.log(properties)
    var t = properties.replace(/'/g, '\"'),
        data = $.parseJSON(t),
        contents = '';
    $.each(data, function(k, v){
        contents += '<div class=\'row\' style=\'margin-top: 10px;\'>';
        contents += '<div class=\'col-xs-1\'></div>';
        contents += '<div class=\'col-xs-4\'><label>{0}: </label></div>'.format(k);
        contents += '<div class=\'col-xs-7\'><input name=\'{0}\' value=\'{1}\'/></div>'.format(k, v);
        contents += '</div>';
    });
    $(location).html(contents);
}

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
            $('.moduleNodeDetail').find('input[name="moduleNodeDetailId"]').val(params.nodes);
            $('#node-detail-modal').modal('show');
        }
    })

}