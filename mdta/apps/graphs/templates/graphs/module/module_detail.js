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
$('.moduleEdgeEditForm #moduleEdgeEditType').on('change', function(){
    var edge_type_id = $(this).find('option:selected').val(),
        location = $(this).closest('.moduleEdgeEditForm').find('#module-edge-edit-properties');

    load_keys_from_node_edge_type(edge_type_id, location, 'edge');
});

$('.moduleEdgeEditForm').on('submit', function(e){
    var name = $(e.currentTarget).find('input[name="moduleEdgeEditName"]').val(),
        location = $(e.currentTarget).find('#moduleEdgeEditErrMessage');

    if (name == ''){
        showErrMsg(location, 'Name is Empty');
        return false;
    }
});
/* End Module Edge Edit Code */

function load_keys_from_node_edge_type(item_id, location, type){
    $.getJSON("{% url 'graphs:get_keys_from_type' %}?id={0}&type={1}".format(item_id, type)).done(function(data){
        var contents = '';
        $.each(data, function(k, v){
            contents += '<div class=\'row\' style=\'margin-top: 5px;\'>';
			contents += '<div class=\'col-xs-4\'><label>{0}: </label></div>'.format(data[k]);
			contents += '<div class=\'col-xs-8\'><input name=\'{0}\'/></div>'.format(data[k]);
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
            $('a[href="#moduleNodeEdit"]').click();
            $('a[href="#node-{0}"]'.format(params.nodes)).click();
        } else if (!$.isEmptyObject(params.edges)) {
            $('a[href="#moduleEdgeEdit"]').click();
            $('a[href="#edge-{0}"]'.format(params.edges)).click();
        }
    })

}