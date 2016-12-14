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
        properties = $(e.currentTarget).find('#module-node-edit-properties input'),
        item = '',
        item_str = '',
        is_json_format = true,
        json_msg = '',
        data = '';

    if (name == ''){
        showErrMsg(location, 'Name is Empty');
        return false;
    }

    $.each(properties, function(index){
        item = properties[index];
        if (item.name.indexOf('Inputs_') >= 0 || item.name.indexOf('Outputs_') >= 0) {
            item_str = item.value.replace(/'/g, '"');
            if (!isJsonFormat(item_str)){
                if (item_str.length > 0){
                    json_msg = 'JSON format incorrect: {0}'.format(item.name);
                } else {
                    json_msg = 'JSON input empty: {0}'.format(item.name);
                }
                is_json_format = false;
                return false;
            }
        }
    });

    if (!is_json_format) {
        showErrMsg(location, json_msg);
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
        is_json_format = '',
        submit = $(e.currentTarget).find('button[type="submit"]:focus');

    //console.log(edge_type)

    $.each(properties, function(index){
        if (properties[index].name != 'Invisible') {
            var str = properties[index].value.replace(/'/g, '"');
            //console.log(str.length)
            if (str.length > 0){
                properties_no_input = false;
                is_json_format = isJsonFormat(str);
                return false;
            }
        }
    });

    if (properties_no_input && edge_type != 'Connector' && submit[0].textContent == 'Save'){
        showErrMsg(location, 'Input of property empty');
        return false;
    }
    if (!is_json_format){
        showErrMsg(location, 'JSON format incorrect.');
        return false;
    }
});

function isJsonFormat(str){
    var is_json = true;
    try {
        var json = $.parseJSON(str);
    } catch(e){
        is_json = false
    }
    return is_json
}
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
        height: '800px',
        physics: {
            barnesHut: {
                gravitationalConstant: -4000
            }
        }
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
        } else {
            $('a[href="#moduleNodeEdgeEmpty"]').click();
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
                     $('body').css('cursor', 'progress');
                }
            })
        }
    })

}


/* Start Node Name for OnFailGoTo of MenuPrompt Code */

$('.moduleNodeEditForm input[name="OnFailGoTo"]').autocomplete({
    source: node_names_autocomplete
});

/* End   Node Name for OnFailGoTo of MenuPrompt Code */