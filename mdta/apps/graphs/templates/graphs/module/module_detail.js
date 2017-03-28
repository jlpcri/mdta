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
        is_json_format = true,
        json_msg = '',
        data = '';

    if (name == ''){
        showErrMsg(location, 'Name is Empty');
        return false;
    }

    var check_json = check_node_properties_json(properties);


    if (!check_json['is_json_format']) {
        showErrMsg(location, check_json['json_msg']);
        return false;
    }

    $(e.currentTarget).find('.moduleNodeEditPropertyTable tbody tr').each(function(){
        data += this.id + ' ';
    });
    $(e.currentTarget).find('input[name="property_data_index"]').val(data);

});

function check_node_properties_json(properties){
    var data = {},
        item = '',
        item_str = '',
        json_msg = '',
        is_json_format = true;

    $.each(properties, function(index){
        item = properties[index];
        if (item.name.indexOf('Inputs_') >= 0 || item.name.indexOf('Outputs_') >= 0 || item.name.indexOf('Variable_') >= 0) {
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

    data['is_json_format'] = is_json_format;
    data['json_msg'] = json_msg;

    return data;
}
/* End Module Node Edit Code */


/* Start Module Edge Edit Code */
$('.moduleEdgeEditForm #moduleEdgeEditType').on('change', function(){
    var edge_type_id = $(this).find('option:selected').val(),
        location = $(this).closest('.moduleEdgeEditForm').find('#module-edge-edit-properties');

    load_keys_from_type_contents(edge_type_id, location, 'edge');
});

$('.moduleEdgeEditForm').on('submit', function(e){
    var location = $(e.currentTarget).find('#moduleEdgeEditErrMessage'),
        properties = $(e.currentTarget).find('#module-edge-edit-properties input'),
        //edge_type = $(e.currentTarget).find('#moduleEdgeEditType option:selected').text(),
        submit = $(e.currentTarget).find('button[type="submit"]:focus');

    //console.log(edge_type)

    var check_json = check_edge_properties_json(properties);

    //if (check_json['properties_no_input'] && edge_type != 'Connector' && submit[0].textContent == 'Save'){
    //    showErrMsg(location, 'Input of property empty');
    //    return false;
    //}

    if (!check_json['is_json_format']){
        showErrMsg(location, check_json['json_msg']);
        return false;
    }
});

function check_edge_properties_json(properties){
    var data = {},
        item = '',
        item_str = '',
        json_msg = '',
        is_json_format = true;

    $.each(properties, function(index){
        item = properties[index];
        if (item.name.indexOf('Outputs_') >= 0 || item.name.indexOf('Condition_') >= 0) {
            item_str = properties[index].value.replace(/'/g, '"');
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

    data['is_json_format'] = is_json_format;
    data['json_msg'] = json_msg;

    return data;
}

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
    autocomplete_nodename_and_edgekeys();
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

    var n = JSON.stringify("{{ network_edges|escapejs }}");
    var edge = JSON.parse(n);
    $.each(JSON.parse(edge), function(idx, obj) {
        var id = obj.id;
        var route = obj.data;
        for (var i = 0; i < route.length; ++i) {
            for (var ind in route[i]) {
                if (ind === 'tcs_cannot_route') {
                    edges.update([{id: id, color: '#FF3333'}])
                }
            }
        }
    });


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
                } else {
                    //if (data['node_data']['type_name'].indexOf('Prompt') >= 0) {
                        open_prompts_modal(data['node_data'], params.nodes);
                    //}
                }
            })
        }
    })
}

function open_prompts_modal(node, node_id){
    //console.log(node['properties'])
    //console.log(node['verbiage'])

    var properties = node['properties'],
        verbiage = node['verbiage'],
        node_in = node['node_in'],
        type_name = node['type_name'],
        node_keys = node['node_keys'],

        language_id = node['language']['id'], // project current test language
        language_name = node['language']['name'],
        language_key = '',

        languages = node['languages'], // all possible languages project has
        properties_contents = '',
        verbiage_contents = '';

    if (language_name != '') {
        language_key = language_name;
    } else {
        language_key = languages[0]['name']
    }

    properties_contents = get_properties_contents(node_keys, properties, node_id, node_in);
    verbiage_contents = get_verbiage_contents(type_name, node['languages'], node['v_keys'], verbiage, language_key);

    //console.log(node['languages'], node['language_id'])

    $('.moduleNodeEdit #moduleNodeEditId').val(node_id);
    $('.moduleNodeEdit #moduleNodeEditName').val(node['name']);
    $('.moduleNodeEdit #moduleNodeEditType').val(node['type_id']);

    $('.moduleNodeEdit #module-node-edit-properties').html(properties_contents);
    $('.moduleNodeEdit #module-node-edit-verbiages').html(verbiage_contents);

    node_property_js_load();

    if (language_id != '') {
        $('.moduleNodeEdit #moduleNodeEditVerbiageLanguage').val(language_id);
    }

    $('.moduleNodeEdit #moduleNodeEditVerbiageLanguage').on('change', function(){
        var language_name = $(this).find('option:selected').text();

        $.each(node['v_keys'], function(k, v){
            //console.log(verbiage)
            if ( verbiage === null || $.isEmptyObject(verbiage) || typeof verbiage[language_name] == 'undefined' || typeof verbiage[language_name][v] == 'undefined') {
                $('.moduleNodeEdit textarea[name="{0}"]'.format(v)).val('');
            } else {
                $('.moduleNodeEdit textarea[name="{0}"]'.format(v)).val(verbiage[language_name][v]);
            }
        })

    });

    $('.moduleNodeEdit #moduleNodeEditType').on('change', function(){
        var type_id = $(this).find('option:selected').val(),
            type_name = $(this).find('option:selected').text(),
            properties_location = $('.moduleNodeEdit #module-node-edit-properties'),
            verbiage_location = $('.moduleNodeEdit #module-node-edit-verbiages'),
            verbiage_contents = '';

        // update Property/Verbiage contents
        $.getJSON("{% url 'graphs:get_keys_from_type' %}?id={0}&type={1}".format(type_id, 'node')).done(function(data){
            //console.log(data)
            properties_contents = get_properties_contents(data['keys'], properties, node_id, node_in);
            verbiage_contents = get_verbiage_contents(type_name, node['languages'], data['v_keys'], verbiage, language_key);

            properties_location.html(properties_contents);
            verbiage_location.html(verbiage_contents);

            node_property_js_load();
        });

    });

    $('a[href="#verbiage"]').click();
    $('#module-node-edit-modal').modal('show');
}

function node_property_js_load(){
    var rowCounter = 0;

    $('.myToggle').bootstrapToggle();
    autocomplete_nodename_and_edgekeys();
    $('#buttonAddData').click(function(){
        rowCounter = parseInt($('tr').last().attr('id'));
        if (! isNaN(rowCounter)){
            rowCounter += 1;
        } else{
            rowCounter = 0;
        }
        node_property_add_data(['Inputs', 'Outputs'], rowCounter, '.moduleNodeEdit table', 'call');
    });
}

function get_properties_contents(node_keys, properties, node_id, node_in){
    var tmp_index = 0,
        object_length = 0,
        properties_contents = '';

    $.each(node_keys, function(index, k){
        if (k == 'InputData'){
            properties_contents += '<table class=\'table ModuleNodeEditPropertyTable\' id=\'node-property-table-{0}\'>'.format(node_id);
            properties_contents += '<thead><tr>';
            properties_contents += '<th class=\'col-xs-5\'>Inputs</th><th class=\'col-xs-5\'>Outputs</th>';
            properties_contents += '<th class=\'col-xs-1\'><button id=\'buttonAddData\' class=\'btn btn-xs\' type=\'button\'>Add data</button></th>';
            properties_contents += '</tr></thead>';
            properties_contents += '<tbody>';
            $.each(properties[k], function(idx, value){
                properties_contents += '<tr id=\'{0}\'>'.format(idx);

                properties_contents += '<td>';
                properties_contents += '<input name=\'Inputs_{0}\' value=\"{'.format(idx);
                tmp_index = 0;
                object_length = Object.keys(value['Inputs']).length;
                $.each(value['Inputs'], function(sk, sv){
                    properties_contents += '\'{0}\': \'{1}\''.format(sk, sv);
                    tmp_index += 1;
                    if (tmp_index < object_length){
                        properties_contents += ', ';
                    }
                });
                properties_contents += '}\">';
                properties_contents += '</td>';

                properties_contents += '<td>';
                properties_contents += '<input name=\'Outputs_{0}\' value=\"{'.format(idx);
                tmp_index = 0;
                object_length = Object.keys(value['Outputs']).length;
                $.each(value['Outputs'], function(sk, sv){
                    properties_contents += '\'{0}\': \'{1}\''.format(sk, sv);
                    tmp_index += 1;
                    if (tmp_index < object_length){
                        properties_contents += ', ';
                    }
                });
                properties_contents += '}\">';
                properties_contents += '</td>';

                properties_contents += '<td class=\'text-center\'><a href=\'#\' onclick=\'deleteRow(this);\'><i class=\'fa fa-trash-o fa-lg\'></i></a></td>';

                properties_contents += '</tr>';
            });
            properties_contents += '</tbody>';
            properties_contents += '</table>';
        } else if (k == 'OutputData'){
            properties_contents += '<div class=\'row\' style=\'margin-top: 5px;\'>';
            properties_contents += '<div class=\'col-xs-4\'><label>{0}:</label></div>'.format('Value');
            properties_contents += '<div class=\'col-xs-8\'><input name=\'{0}\''.format('Variable_0');
            if (typeof properties[k] == 'undefined'){
                properties_contents += 'value=\'\'';
            } else {
                $.each(properties[k]['Variable'], function (key, value) {
                    properties_contents += 'value=\"{\'{0}\': \'{1}\'}\"'.format(key, value);
                });
            }
            properties_contents += '></div>';
            properties_contents += '</div>';
        }else {
            if (!((k == 'Default') && (node_in == 'module'))) {
                properties_contents += '<div class=\'row\' style=\'margin-top: 5px;\'>';
                properties_contents += '<div class=\'col-xs-4\'><label>{0}:</label></div>'.format(k);
                if (k == 'NonStandardFail') {
                    properties_contents += '<div class=\'col-xs-8\'>';
                    if (properties[k] == 'on') {
                        properties_contents += '<input name=\'{0}\' type=\'checkbox\' checked class=\'myToggle\' data-on=\'True\' data-width=\'100\' data-onstyle=\'success\' data-off=\'False\' >'.format(k);
                    } else {
                        properties_contents += '<input name=\'{0}\' type=\'checkbox\' class=\'myToggle\' data-on=\'True\' data-width=\'100\' data-onstyle=\'success\' data-off=\'False\' >'.format(k);
                    }
                    properties_contents += '</div>';
                } else {
                    if (typeof properties[k] == 'undefined'){
                        properties_contents += '<div class=\'col-xs-8\'><input name=\'{0}\' value=\'\'></div>'.format(k);
                    } else {
                        properties_contents += '<div class=\'col-xs-8\'><input name=\'{0}\' value=\'{1}\'></div>'.format(k, properties[k]);
                    }
                }
                properties_contents += '</div>';
            }
        }
    });

    return properties_contents;
}

function get_verbiage_contents(type_name, languages, verbiage_keys, verbiage, language_key){
    var verbiage_contents = '';

    if (type_name.indexOf('Prompt') >= 0) {
        verbiage_contents += '<table class=\'table ModuleNodeEditVerbiageTable\' id=\'node-verbiage-table\'>';
        verbiage_contents += '<thead><tr>';
        verbiage_contents += '<td class=\'col-xs-3\'></td><td class=\'col-xs-9\'></td>';
        verbiage_contents += '</tr></thead><tbody>';

        verbiage_contents += '<tr>';
        verbiage_contents += '<td><label for=\'moduleNodeEditVerbiageLanguage\'>Language:</label></td>';
        verbiage_contents += '<td>';
        verbiage_contents += '<select class=\'form-control\' name=\'moduleNodeEditVerbiageLanguage\' id=\'moduleNodeEditVerbiageLanguage\'>';
        $.each(languages, function (k, v) {
            verbiage_contents += '<option value=\'{0}\'>{1}</option>'.format(v['id'], v['name'])
        });
        verbiage_contents += '</select>';
        verbiage_contents += '</td>';
        verbiage_contents += '</tr>';

        //console.log(verbiage, language_key, verbiage[language_key])
        $.each(verbiage_keys, function (k, v) {
            //console.log(k, v)
            verbiage_contents += '<tr>';
            verbiage_contents += '<td><label>{0}:</label></td>'.format(v);
            if (verbiage === null || $.isEmptyObject(verbiage) || typeof verbiage[language_key] == 'undefined' || typeof verbiage[language_key][v] == 'undefined') {
                verbiage_contents += '<td><textarea name=\'{0}\' rows=\'3\' style=\'width:100%\'></textarea></td>'.format(v);
            } else {
                verbiage_contents += '<td><textarea name=\'{0}\' rows=\'3\' style=\'width:100%\'>{1}</textarea></td>'.format(v, verbiage[language_key][v]);
            }
            verbiage_contents += '</tr>';
        });
        verbiage_contents += '</tbody></table>';
    }

    return verbiage_contents
}

$('.moduleNodeEdit').on('submit', function(e){
    var name = $(e.currentTarget).find('input[name="moduleNodeEditName"]').val(),
        location = $(e.currentTarget).find('#moduleNodeEditErrMessage'),
        properties = $(e.currentTarget).find('#module-node-edit-properties input'),
        is_json_format = true,
        json_msg = '',
        data = '';

    if (name == ''){
        showErrMsg(location, 'Name is Empty');
        return false;
    }

    var check_json = check_node_properties_json(properties);


    if (!check_json['is_json_format']) {
        showErrMsg(location, check_json['json_msg']);
        return false;
    }

    $(e.currentTarget).find('#module-node-edit-properties table tbody tr').each(function(){
        data += this.id + ' ';
    });
    $(e.currentTarget).find('input[name="property_data_index"]').val(data);

});

/* Start Node Name for OnFailGoTo of MenuPrompt Code */

function autocomplete_nodename_and_edgekeys(call_from) {
    var myToggle = $('.myToggle'),
        project_node_new_fail = $('.projectNodeNew input[name="OnFailGoTo"]'),
        module_node_edit_fail = $('.moduleNodeEditForm input[name="OnFailGoTo"]'),
        node_edge_new_fail = $('.moduleNodeEdgeNew input[name="node_OnFailGoTo"]'),

        node_data_modal_edit_fail = $('.moduleNodeEdit input[name="OnFailGoTo"]'),

        project_node_new_outputs = $('.projectNodeNew input[name="Outputs"]'),
        module_node_edit_outputs = $('.moduleNodeEditForm input[name="Outputs"]'),
        node_edge_new_outputs = $('.moduleNodeEdgeNew input[name="node_Outputs"]'),
        data_edge_keys = $('.data_edge_keys');

    switch (call_from){
        case 'node':
            myToggle.bootstrapToggle();
            project_node_new_fail.autocomplete({
                source: node_names_autocomplete
            });
            module_node_edit_fail.autocomplete({
                source: node_names_autocomplete
            });

            project_node_new_outputs.autocomplete({
                source: menu_prompt_outputs_keys_autocomplete
            });
            module_node_edit_outputs.autocomplete({
                source: menu_prompt_outputs_keys_autocomplete
            });

            data_edge_keys.autocomplete({
                source: data_edge_keys_autocomplete
            });
            break;
        case 'auto_node':
            myToggle.bootstrapToggle();
            node_edge_new_fail.autocomplete({
                source: node_names_autocomplete
            });
            node_edge_new_outputs.autocomplete({
                source: menu_prompt_outputs_keys_autocomplete
            });
            break;
        case 'edge':
            myToggle.bootstrapToggle();
            data_edge_keys.autocomplete({
                source: data_edge_keys_autocomplete
            });
            break;
        case 'auto_edge':
            myToggle.bootstrapToggle();
            data_edge_keys.autocomplete({
                source: data_edge_keys_autocomplete
            });
            break;
        default:
            project_node_new_fail.autocomplete({
                source: node_names_autocomplete
            });
            module_node_edit_fail.autocomplete({
                source: node_names_autocomplete
            });
            node_data_modal_edit_fail.autocomplete({
                source: node_names_autocomplete
            });

            project_node_new_outputs.autocomplete({
                source: menu_prompt_outputs_keys_autocomplete
            });
            module_node_edit_outputs.autocomplete({
                source: menu_prompt_outputs_keys_autocomplete
            });

            data_edge_keys.autocomplete({
                source: data_edge_keys_autocomplete
            });
    }
}


/* End   Node Name for OnFailGoTo of MenuPrompt Code */