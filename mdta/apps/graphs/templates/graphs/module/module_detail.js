/**
 * Created by sliu on 6/8/16.
 */

$('.moduleNodeNew form').on('submit', function(){
    var name = $('.moduleNodeNew #id_name').val();
    if (name == ''){
        showErrMsg('#moduleNodeNewErrMessage', 'Name is Empty.');
        return false;
    }
});

$('.moduleNodeNew #id_type').on('change', function(){
    var item_id = $(this).find('option:selected').val(),
        location = '#module-node-new-properties';
    load_keys_from_node_edge_type(item_id, location, 'node');
});

$('.moduleNodeEdit').on('show.bs.modal', function(e){
    var node_id = $(e.relatedTarget).data('node-id'),
        node_name = $(e.relatedTarget).data('node-name');

    $(e.currentTarget).find('input[name="moduleNodeEditId"]').val(node_id);
    $(e.currentTarget).find('input[name="moduleNodeEditName"]').val(node_name);
    $('.moduleNodeEdit .modal-title').html('Node Edit/Delete');
});

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

$(document).ready(function(){
    var node_type_id = $('.moduleNodeNew #id_type').find('option:selected').val(),
        node_location = '#module-node-new-properties';

    if (node_type_id) {
        load_keys_from_node_edge_type(node_type_id, node_location, 'node');
    }

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
            shape: 'ellipse',
            //fontSize: 10
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
}