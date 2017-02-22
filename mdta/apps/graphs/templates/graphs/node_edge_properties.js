var toggle_style_key_list = ['NonStandardFail', 'Invisible', 'NoneConfirm'];

function load_keys_from_type_contents(item_id, location, type, call_from_node_edit){
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
                contents += '<table class=\'table moduleNodeEditPropertyTable\' id=\'{0}-property-table\'>'.format(type);

                contents += '<thead><tr>';
                $.each(subkeys, function(k, v){
                    if (type == 'edge' && subkeys[k] == 'Outputs'){
                        contents += '<th class=\'col-xs-5\'>{0}</th>'.format('Follow If...');
                    } else {
                        contents += '<th class=\'col-xs-5\'>{0}</th>'.format(subkeys[k]);
                    }
                });
                if (keys[k].indexOf('InputData') >= 0) {
                    contents += '<th class=\'col-xs-1\'><button id=\'buttonAddData\' class=\'btn btn-xs\' type=\'button\'>Add Data</button></th>';
                } else {
                    contents += '<th class=\'col-xs-1\'></th>';
                }
                contents += '</tr></thead>';

                contents += '<tbody>';

                contents += '<tr id=\'{0}\'>'.format(rowCounter);
                if (call_from_node_edit) {
                    $.each(subkeys, function (k, v) {
                        if (type == 'edge' && subkeys[k] == 'Outputs'){
                            contents += '<td><input name=\'{0}_{1}\' class=\'data_edge_keys\' placeholder={2}/></td>'.format(subkeys[k], rowCounter, place_holder_json);
                        } else {
                            contents += '<td><input name=\'{0}_{1}\' placeholder={2}/></td>'.format(subkeys[k], rowCounter, place_holder_json);
                        }
                    });
                } else {
                    $.each(subkeys, function (k, v) {
                        if (type == 'edge' && subkeys[k] == 'Outputs'){
                            contents += '<td><input name=\'{0}_{1}\' class=\'data_edge_keys\' style=\'width:100%\' placeholder={2}/></td>'.format(subkeys[k], rowCounter, place_holder_json);
                        } else {
                            contents += '<td><input name=\'{0}_{1}\' style=\'width:100%\' placeholder={2}/></td>'.format(subkeys[k], rowCounter, place_holder_json);
                        }
                    });
                }
                contents += '</tr>';

                contents += '</tbody></table>';
                contents += '</div>';
                contents += '</div>';
            } else {
                contents += '<div class=\'row\' style=\'margin-top: 0px;\'>';
                contents += '<div class=\'col-xs-1\'></div>';
                contents += '<div class=\'col-xs-11\'><label>{0}: </label></div>'.format(keys[k]);
                contents += '</div>';
                contents += '<div class=\'row\' style=\'margin-top: 0px;\'>';
                contents += '<div class=\'col-xs-1\'></div>';
                if (call_from_node_edit){
                    if (toggle_style_key_list.indexOf(keys[k]) >= 0){
                        contents += '<div class=\'col-xs-11\'><input name=\'{0}\' type=\'checkbox\' class=\'myToggle\' data-on=\'True\' data-width=\'100\' data-onstyle=\'success\' data-off=\'False\'/></div>'.format(keys[k]);
                    } else {
                        contents += '<div class=\'col-xs-11\'><input name=\'{0}\' style=\'width:110%\' placeholder=\'{1}\'/></div>'.format(keys[k], get_placeholder(keys[k]));
                    }
                } else {
                    if (toggle_style_key_list.indexOf(keys[k]) >= 0){
                        contents += '<div class=\'col-xs-11\'><input name=\'{0}\' type=\'checkbox\' class=\'myToggle\' data-on=\'True\' data-width=\'100\' data-onstyle=\'success\' data-off=\'False\'/></div>'.format(keys[k]);
                    } else {
                        contents += '<div class=\'col-xs-11\'><input name=\'{0}\' style=\'width:80%\' placeholder=\'{1}\'/></div>'.format(keys[k], get_placeholder(keys[k]));
                    }
                }
                contents += '</div>';
            }
        });
        //console.log(contents)
        $(location).html(contents);

        autocomplete_nodename_and_edgekeys(type);

        $('#buttonAddData').click(function(){
            rowCounter++;
            node_property_add_data(subkeys, rowCounter, '.moduleNodeEditPropertyTable', call_from_node_edit);
        });
    });
}

function node_property_add_data(subkeys, rowCounter, location, call_from_node_edit){
    var newRow = '';

    newRow += '<tr id=\'{0}\'>'.format(rowCounter);
    if (call_from_node_edit) {
        $.each(subkeys, function (k, v) {
            newRow += '<td><input name=\'{0}_{1}\' placeholder={2}/></td>'.format(subkeys[k], rowCounter, place_holder_json);
        });
    } else {
        $.each(subkeys, function (k, v) {
            newRow += '<td><input name=\'{0}_{1}\' style=\'width:100%\' placeholder={2}/></td>'.format(subkeys[k], rowCounter, place_holder_json);
        });
    }
    newRow += '<td class=\'text-center\'><a href=\'#\' onclick=\'deleteRow(this);\'><i class=\'fa fa-trash-o fa-lg\'></i></a></td>';
    newRow += '</tr>';
    $(location).append(newRow)
}

function deleteRow(row){
    $(row).closest('tr').remove();
}


function module_node_edit_add_data(node_id){
    var subkeys = ['Inputs', 'Outputs'],
        location = '#node-property-table-{0}'.format(node_id);

    var rowCounter = parseInt($('{0} tr:last'.format(location)).attr('id')) + 1;

    node_property_add_data(subkeys, rowCounter, location);
}

function get_placeholder(key){
    var data = '{prompt}';
    switch (key){
        case 'NoInput_1':
            data += 'NI1';
            break;
        case 'NoInput_2':
            data += 'NI2';
            break;
        case 'NoMatch_1':
            data += 'NM1';
            break;
        case 'NoMatch_2':
            data += 'NM2';
            break;
        case 'ConfirmNoInput_1':
            data += 'CNI1';
            break;
        case 'ConfirmNoInput_2':
            data += 'CNI2';
            break;
        case 'ConfirmNoMatch_1':
            data += 'CNM1';
            break;
        case 'ConfirmNoMatch_2':
            data += 'CNM2';
            break;
        default :
            data = ''
    }

    return data
}