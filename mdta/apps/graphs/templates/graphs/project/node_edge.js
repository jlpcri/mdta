/**
 * Created by sliu on 5/18/16.
 */
$('.projectNodeNew #id_type').on('change', function(){
    var item_id = $(this).find('option:selected').val(),
        location = '#project-node-new-data-input';
    load_keys_from_type_contents(item_id, location, 'node');
});

$('.projectEdgeNew #id_type').on('change', function(){
    var item_id = $(this).find('option:selected').val(),
        location = '#project-edge-new-data-input';
    load_keys_from_type_contents(item_id, location, 'edge');
});

$(document).ready(function(){
    var node_id = $('.projectNodeNew #id_type').find('option:selected').val(),
        edge_id = $('.projectEdgeNew #id_type').find('option:selected').val(),
        node_location = '#project-node-new-data-input',
        edge_location = '#project-edge-new-data-input';
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