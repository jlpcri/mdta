/**
 * Created by sliu on 6/8/16.
 */



/* Start Module Node Edit Code */
$('.moduleNodeEditForm #moduleNodeEditType').on('change', function(e){
    var type_id = $(this).find('option:selected').val(),
        location = $(this).closest('.moduleNodeEditForm').find('#module-node-edit-properties');

    load_keys_from_type_contents(type_id, location, 'node', 'module_node_edit');
});

$('.moduleNodeEditForm').on('submit', function(e){
    var name = $(e.currentTarget).find('input[name="moduleNodeEditName"]').val(),
        location = $(e.currentTarget).find('#moduleNodeEditErrMessage'),
        data = '';

    if (name == ''){
        showErrMsg(location, 'Name is Empty');
        return false;
    }

    $(e.currentTarget).find('.moduleNodeEditPropertyTable tbody tr').each(function(){
        data += this.id + ' ';
    });
    $(e.currentTarget).find('input[name="property_data_index"]').val(data);
});
/* End Module Node Edit Code */


/* Start Module Edge Edit Code */
$('.moduleEdgeEditForm #moduleEdgeEditType').on('change', function(){
    var edge_type_id = $(this).find('option:selected').val(),
        location = $(this).closest('.moduleEdgeEditForm').find('#module-edge-edit-properties');

    load_keys_from_type_contents(edge_type_id, location, 'edge');
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
    });

    network.on('doubleClick', function(params){
        if (!$.isEmptyObject(params.nodes)){
            $.getJSON("{% url 'graphs:get_module_id_from_node_id' %}?node_id={0}".format(params.nodes)).done(function(data){
                //console.log(data);
                var base_url = '',
                    tmp = window.location.href.split('/'),
                    current_module_id = tmp[tmp.length - 2];

                for (var i = 0; i < tmp.length - 2; i++) {
                    base_url += tmp[i] + '/'
                }
                if (!( data['module_id'] == current_module_id)){
                    window.location.href = base_url + data['module_id'];
                     $('body').css('cursor', 'wait');
                }
            })
        }
    })

}