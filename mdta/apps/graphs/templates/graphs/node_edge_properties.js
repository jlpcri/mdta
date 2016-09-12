function load_keys_from_type_contents(item_id, location, type){
    $.getJSON("{% url 'graphs:get_keys_from_type' %}?id={0}&type={1}".format(item_id, type)).done(function(data){
        var keys = data['keys'],
            subkeys = data['subkeys'],
            rowCounter = 0,
            contents = '';
        $.each(keys, function(k, v){
            if ((keys[k].indexOf('Data') >= 0) ) {
                contents += '<div class=\'row\' style=\'margin-top: 5px;\'>';
                contents += '<div class=\'col-xs-3\'><label>{0}: </label></div>'.format(keys[k]);
                contents += '</div>';

                contents += '<div class=\'row\' style=\'margin-top: 5px;\'>';
                contents += '<div class=\'col-xs-1\'></div>';
                contents += '<div class=\'col-xs-11\'>';
                contents += '<table class=\'table\' id=\'{0}-property-table\'>'.format(type);

                contents += '<thead><tr>';
                $.each(subkeys, function(k, v){
                    contents += '<th class=\'col-xs-5\'>{0}</th>'.format(subkeys[k]);
                });
                if (keys[k].indexOf('InputData') >= 0) {
                    contents += '<th class=\'col-xs-1\'><button id=\'buttonAddData\' class=\'btn btn-xs\' type=\'button\'>Add Data</button></th>';
                } else {
                    contents += '<th class=\'col-xs-1\'></th>';
                }
                contents += '</tr></thead>';

                contents += '<tbody>';

                contents += '<tr id=\'{0}\'>'.format(rowCounter);
                $.each(subkeys, function(k, v){
                    contents += '<td><input name=\'{0}_{1}\'/></td>'.format(subkeys[k], rowCounter);
                });
                contents += '</tr>';

                contents += '</tbody></table>';
                contents += '</div>';
                contents += '</div>';
            } else {
                contents += '<div class=\'row\' style=\'margin-top: 5px;\'>';
                contents += '<div class=\'col-xs-3\'><label>{0}: </label></div>'.format(keys[k]);
                contents += '<div class=\'col-xs-2\'><input name=\'{0}\'/></div>'.format(keys[k]);
                contents += '</div>';
            }
        });
        //console.log(contents)
        $(location).html(contents);

        $('#buttonAddData').click(function(){
            rowCounter++;
            node_property_add_data(subkeys, rowCounter);
        });
    });
}

function node_property_add_data(subkeys, rowCounter){
    var newRow = '';

    newRow += '<tr id=\'{0}\'>'.format(rowCounter);
    $.each(subkeys, function(k, v){
        newRow += '<td><input name=\'{0}_{1}\'/></td>'.format(subkeys[k], rowCounter);
    });
    newRow += '<td class=\'text-center\'><a href=\'#\' onclick=\'deleteRow(this);\'><i class=\'fa fa-trash-o fa-lg\'></i></a></td>';
    newRow += '</tr>';
    $('#node-property-table').append(newRow)
}

function deleteRow(row){
    $(row).closest('tr').remove();
}
