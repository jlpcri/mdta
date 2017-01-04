/* Start Module Node New Node & Edge Code */
function load_keys_from_type_contents_edge_auto(item_id, location, type){
    $.getJSON("{% url 'graphs:get_keys_from_type' %}?id={0}&type={1}".format(item_id, type)).done(function(data){
        var keys = data['keys'],
            subkeys = data['subkeys'],
            rowCounter = 0,
            contents = '';
        $.each(keys, function(k, v){
            if ((keys[k].indexOf('Data') >= 0) || (keys[k] == 'Condition')) {
                //contents += '<div class=\'row\' style=\'margin-top: 5px;\'>';
                //contents += '<div class=\'col-xs-3\'><label>{0}: </label></div>'.format(keys[k]);
                //contents += '</div>';

                contents += '<div class=\'row\' style=\'margin-top: 5px;\'>';
                contents += '<div class=\'col-xs-1\'></div>';
                contents += '<div class=\'col-xs-11\'>';
                contents += '<table class=\'table\' id=\'{0}-together-property-table\'>'.format(type);

                contents += '<thead><tr>';
                $.each(subkeys, function(k, v){
                    if (subkeys[k] == 'Outputs'){
                        contents += '<th class=\'col-xs-2\'>{0}</th>'.format('Follow If...');
                    } else {
                        contents += '<th class=\'col-xs-2\'>{0}:</th>'.format(subkeys[k]);
                    }
                });
                contents += '<th class=\'col-xs-2\'></th>';
                contents += '</tr></thead>';

                contents += '<tbody>';

                contents += '<tr id=\'{0}\'>'.format(rowCounter);
                $.each(subkeys, function(k, v){
                    if (subkeys[k] == 'Outputs'){
                        contents += '<td><input name=\'edge_{0}_{1}\' class=\'data_edge_keys\' style=\'width:120%\' placeholder={2}/></td>'.format(subkeys[k], rowCounter, place_holder_json);
                    } else {
                        contents += '<td><input name=\'edge_{0}_{1}\' style=\'width:120%\' placeholder={2}/></td>'.format(subkeys[k], rowCounter, place_holder_json);
                    }
                });
                contents += '</tr>';

                contents += '</tbody></table>';
                contents += '</div>';
                contents += '</div>';
            } else {
                contents += '<div class=\'row\' style=\'margin-top: 5px;\'>';
                contents += '<div class=\'col-xs-1\'></div>';
                contents += '<div class=\'col-xs-3\'><label>{0}: </label></div>'.format(keys[k]);
                if (keys[k] == 'Invisible'){
                    contents += '<div class=\'col-xs-8\'><input name=\'edge_{0}\' type=\'checkbox\' data-toggle=\'toggle\' class=\'myToggle\' data-on=\'True\' data-width=\'100\' data-onstyle=\'success\' data-off=\'False\' style=\'width:80% align:left\' /></div>'.format(keys[k]);
                } else {
                    contents += '<div class=\'col-xs-8\'><input name=\'edge_{0}\' style=\'width:80%\' /></div>'.format(keys[k]);
                }
                contents += '</div>';
            }
        });
        //console.log(contents)
        $(location).html(contents);

        autocomplete_nodename_and_edgekeys('auto_' + type)
    });
}

$('.moduleNodeEdgeNew').on('show.bs.modal', function(e){
    var node_type_id = $('.moduleNodeEdgeNew #id_type').find('option:selected').val(),
        node_location = '#module-node-edge-new-node-properties',
        edge_type_id = $('.moduleNodeEdgeNew #id_edge-type').find('option:selected').val(),
        edge_location = '#module-node-edge-new-edge-properties',
        from_node_id = $(e.relatedTarget).data('from-node-id'),
        module_id = $(e.relatedTarget).data('module-id');

    $(e.currentTarget).find('input[name="from_node_id"]').val(from_node_id);
    $(e.currentTarget).find('select[name="module"]').val(module_id);

    load_keys_from_type_contents_node_auto(node_type_id, node_location, 'node');
    load_keys_from_type_contents_edge_auto(edge_type_id, edge_location, 'edge');
});

$('.moduleNodeEdgeNew #id_type').on('change', function(){
    var node_type_id = $(this).find('option:selected').val(),
        location = '#module-node-edge-new-node-properties';

    load_keys_from_type_contents_node_auto(node_type_id, location, 'node');
});

$('.moduleNodeEdgeNew #id_edge-type').on('change', function(){
    var edge_type_id = $(this).find('option:selected').val(),
        location = '#module-node-edge-new-edge-properties';

    load_keys_from_type_contents_edge_auto(edge_type_id, location, 'edge');
});

$('.moduleNodeEdgeNew').on('submit', function(e){
    var node_name = $('.moduleNodeEdgeNew #id_name').val(),
        node_properties = $(e.currentTarget).find('#module-node-edge-new-node-properties input'),
        err_location = '#moduleNodeEdgeNewErrMessage',
        edge_type = $('.moduleNodeEdgeNew #id_edge-type option:selected').text(),
        edge_properties = $(e.currentTarget).find('#module-node-edge-new-edge-properties input'),
        edge_properties_no_input = true,
        data_index_node = '',
        data_index_edge = '';

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

    var check_json_node = check_node_properties_json(node_properties),
        check_json_edge = check_edge_properties_json(edge_properties);

    if (!check_json_node['is_json_format']) {
        showErrMsg(err_location, 'Node ' + check_json_node['json_msg']);
        return false;
    }

    if (!check_json_edge['is_json_format']){
        showErrMsg(err_location, 'Edge ' + check_json_edge['json_msg']);
        return false;
    }

    $('#node-together-property-table tbody tr').each(function(){
        data_index_node += this.id + ' ';
    });
    $('input[name="node_property_data_index"]').val(data_index_node);

    $('#edge-together-property-table tbody tr').each(function(){
        data_index_edge += this.id + ' ';
    });
    $('input[name="edge_property_data_index"]').val(data_index_edge);
});

/* End Module Node New Node & Edge Code */


function load_keys_from_type_contents_node_auto(item_id, location, type, call_from_node_edit){
    $.getJSON("{% url 'graphs:get_keys_from_type' %}?id={0}&type={1}".format(item_id, type)).done(function(data){
        var keys = data['keys'],
            subkeys = data['subkeys'],
            rowCounter = 0,
            contents = '';
        $.each(keys, function(k, v){
            if ((keys[k].indexOf('Data') >= 0) ) {
                //contents += '<div class=\'row\' style=\'margin-top: 5px;\'>';
                //contents += '<div class=\'col-xs-3\'><label>{0}: </label></div>'.format(keys[k]);
                //contents += '</div>';

                contents += '<div class=\'row\' style=\'margin-top: 5px;\'>';
                contents += '<div class=\'col-xs-1\'></div>';
                contents += '<div class=\'col-xs-11\'>';
                contents += '<table class=\'table moduleNodeEditPropertyTable\' id=\'{0}-together-property-table\'>'.format(type);

                contents += '<thead><tr>';
                $.each(subkeys, function(k, v){
                    contents += '<th class=\'col-xs-5\'>{0}</th>'.format(subkeys[k]);
                });
                if (keys[k].indexOf('InputData') >= 0) {
                    contents += '<th class=\'col-xs-1\'><button id=\'buttonTogetherAddData\' class=\'btn btn-xs\' type=\'button\'>Add Data</button></th>';
                } else {
                    contents += '<th class=\'col-xs-1\'></th>';
                }
                contents += '</tr></thead>';

                contents += '<tbody>';

                contents += '<tr id=\'{0}\'>'.format(rowCounter);
                if (call_from_node_edit) {
                    $.each(subkeys, function (k, v) {
                        contents += '<td><input name=\'{0}_{1}\' placeholder={2}/></td>'.format(subkeys[k], rowCounter, place_holder_json);
                    });
                } else {
                    $.each(subkeys, function (k, v) {
                        contents += '<td><input name=\'node_{0}_{1}\' style=\'width:100%\' placeholder={2}/></td>'.format(subkeys[k], rowCounter, place_holder_json);
                    });
                }
                contents += '</tr>';

                contents += '</tbody></table>';
                contents += '</div>';
                contents += '</div>';
            } else {
                contents += '<div class=\'row\' style=\'margin-top: 5px;\'>';
                contents += '<div class=\'col-xs-1\'></div>';
                contents += '<div class=\'col-xs-3\'><label>{0}: </label></div>'.format(keys[k]);
                if (keys[k] == 'NonStandardFail'){
                    contents += '<div class=\'col-xs-8\'><input name=\'node_{0}\' type=\'checkbox\' data-toggle=\'toggle\' class=\'myToggle\' data-on=\'True\' data-width=\'100\' data-onstyle=\'success\' data-off=\'False\' style=\'width:80% align:left;\' /></div>'.format(keys[k]);
                } else {
                    contents += '<div class=\'col-xs-8\'><input name=\'node_{0}\' style=\'width:80%\' placeholder=\'{1}\' /></div>'.format(keys[k], get_placeholder(keys[k]));
                }
                contents += '</div>';
            }
        });
        //console.log(contents)
        $(location).html(contents);

        autocomplete_nodename_and_edgekeys('auto_' + type);

        $('#buttonTogetherAddData').click(function(){
            rowCounter++;
            node_property_add_data_auto(subkeys, rowCounter, '.moduleNodeEditPropertyTable', call_from_node_edit);
        });
    });
}

function node_property_add_data_auto(subkeys, rowCounter, location, call_from_node_edit){
    var newRow = '';

    newRow += '<tr id=\'{0}\'>'.format(rowCounter);
    if (call_from_node_edit) {
        $.each(subkeys, function (k, v) {
            newRow += '<td><input name=\'{0}_{1}\' placeholder={2}/></td>'.format(subkeys[k], rowCounter, place_holder_json);
        });
    } else {
        $.each(subkeys, function (k, v) {
            newRow += '<td><input name=\'node_{0}_{1}\' style=\'width:100%\' placeholder={2}/></td>'.format(subkeys[k], rowCounter, place_holder_json);
        });
    }
    newRow += '<td class=\'text-center\'><a href=\'#\' onclick=\'deleteRow(this);\'><i class=\'fa fa-trash-o fa-lg\'></i></a></td>';
    newRow += '</tr>';
    $(location).append(newRow)
}

function deleteRow(row){
    $(row).closest('tr').remove();
}
