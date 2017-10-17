/**
 * Created by sliu on 8/3/17.
 */
var cy_nodes_default = [],
    cy_edges_default = [],
    cy_edges_gap = [],
    cy_layout_options = '',
    cy_layout_flag = true;  // all nodes have position

$.each(cy_data_nodes, function(key, value){
    //console.log(key, value)
    var posx = 0,
        posy = 0;
    if (!value['positions']){
        posx = key * 100;
        posy = key * 100;
        if (cy_layout_flag) {
            cy_layout_flag = false;
        }
    } else{
        posx = value['positions']['posx'];
        posy = value['positions']['posy']
    }

    cy_nodes_default.push({
        'data': {
            'id': value['id'],
            'label': value['label'],
            'image': image_url + 'mdta-shapes/' + value['image'] + '.png',
            'color': value['color']
        },
        'renderedPosition': {
            x: posx,
            y: posy
        }
    })
});

if (cy_layout_flag){
    cy_layout_options = {
        name: 'preset',
        fit: false
    }
} else {
    cy_layout_options = {
        name: 'breadthfirst',
        fit: true,
        directed: true,
        padding: 30
    }
}

$.each(cy_data_edges, function(key, value){
    //console.log(value),
    cy_edges_default.push({
        'data': {
            'id': value['id'],
            'source': value['from'],
            'target': value['to'],
            'name': value['name'],
            'color': '#00134d'
        }
    })
});

var cy = create_cy_object(cy_nodes_default, cy_edges_default);

function create_cy_object(cy_nodes, cy_edges) {
    add_new_nodes_shape_to_graph(cy_nodes);

    var obj = cytoscape({
        container: $('#node_in_module_cy')[0],
        elements: {
            nodes: cy_nodes,
            edges: cy_edges
        },
        style: [
            {
                selector: 'node[id > 0]',
                style: {
                    'background-image': 'data(image)',
                    'background-color': 'data(color)',
                    'background-fit': 'contain',
                    'shape': 'rectangle',
                    'height': '30px',
                    'width': '75px',
                    'label': 'data(label)',
                    'text-valign': 'bottom',
                    // 'text-wrap': 'ellipsis',
                    // 'text-max-width': '75px'
                }
            },
            {
                selector: 'node[id < 0]',
                style: {
                    'background-image': 'data(image)',
                    'background-color': 'data(color)',
                    'background-fit': 'contain',
                    'shape': 'rectangle',
                    'height': '30px',
                    'width': '75px',
                    // 'label': 'data(label)',
                    // 'text-valign': 'bottom',
                    // 'text-wrap': 'ellipsis',
                    // 'text-max-width': '75px'
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': 1,
                    'line-color': 'data(color)',
                    'curve-style': 'bezier',
                    'target-arrow-color': '#00134d',
                    'target-arrow-shape': 'triangle'
                }
            },
            {
                selector: 'edge:selected',
                style: {
                    'width': 3
                }
            }
        ],
        layout: cy_layout_options,
        userZoomingEnabled: true,
        boxSelectionEnabled: true
    });

    module_context_menu(obj);
    module_click_event(obj);
    module_qtip_event(obj);

    return obj;
}

module_view_options();

function module_context_menu(obj){
    obj.contextMenus({
        menuItems: [
            {
                id: 'verbiages',
                content: 'Verbiages',
                tooltipText: 'Prompt Verbiages',
                selector: 'node[id > 0]',
                onClickFunction: function (event) {
                    var node = event.target;
                    // console.log('Verbiages: ', node.id());

                    $.getJSON("{% url 'graphs:get_module_id_from_node_id' %}?node_id={0}".format(node.id())).done(function(data){
                        open_prompts_modal(data['node_data'], node.id());
                    })
                },
                hasTrailingDivider: true
            },
            {
                id: 'switch-module',
                content: 'Switch Module',
                tooltip: 'Switch to Module',
                selector: 'node[color = "rgb(211, 211, 211)"]',
                onClickFunction: function (event) {
                    var node = event.target;
                    // console.log('Verbiages: ', node.id());

                    $.getJSON("{% url 'graphs:get_module_id_from_node_id' %}?node_id={0}".format(node.id())).done(function(data){
                        var base_url = '',
                            tmp = window.location.href.split('/');

                        for (var i = 0; i < tmp.length - 2; i++) {
                            base_url += tmp[i] + '/'
                        }
                        window.location.href = base_url + data['module_id'];
                        $('body').css('cursor', 'progress');

                    })
                },
                hasTrailingDivider: true
            },
            {
                id: 'remove-node',
                content: 'Remove Node',
                tooltipText: 'Remove Node',
                selector: 'node[id > 0]',
                onClickFunction: function (event) {
                    var node = event.target;
                    remove_node_from_module(node);
                },
                hasTrailingDivider: true
            },
            {
                id: 'new-node',
                content: 'New Node',
                tooltipText: 'Add New Node',
                coreAsWell: true,
                onClickFunction: function (event) {
                    add_new_node_to_module(event.position)
                }
            },
            {
                id: 'new-edge',
                content: 'New Edge',
                tooltipText: 'Add New Edge',
                coreAsWell: true,
                onClickFunction: function (event) {
                    add_new_edge_to_module(event.position);
                }
            },
            {
                id: 'remove-edge',
                content: 'Remove Edge',
                tooltipText: 'Remove Edge',
                selector: 'edge',
                onClickFunction: function (event) {
                    var edge = event.target;
                    remove_edge_from_module(edge);
                },
                hasTrailingDivider: true
            }
        ]
    });
}

function module_click_event(obj){
    var tap_flag = false;

    obj.on('tap', 'node[id > 0]', function(evt){
        var node = evt.target,
            current_module_id = get_current_module_id();;

        $.getJSON("{% url 'graphs:get_module_id_from_node_id'%}?node_id={0}".format(node.id())).done(function(data){
            //var current_module_id = get_current_module_id();

            if (data['module_id'] == current_module_id){
                $('#select_node_id').val(node.id())
            } else {
                $('#select_node_id').val('-1')
            }
        });
        //console.log(node.position())
        $('input[name="Positions"]').val(JSON.stringify({
            'module_id': current_module_id,
            'positions':node.position()
        }));
        // $('a[href="#moduleNodeEdit"]').click();
        $('a[href="#node-{0}"]'.format(node.id())).click();
        $('#module-node-detail-modal').modal('show');
    });

    obj.on('tapend', 'node[id > 0]', function (evt) {
        var node = evt.target;

        // console.log(node.position())
        var data = {
            'node_id': node.id(),
            'position': node.position()
        };
        sendMessage(JSON.stringify(data))
    });

    obj.on('tap', 'node[id < 0]', function (evt) {
        tap_flag = true;
    });

    obj.on('free', 'node[id < 0]', function (evt) {
        var node_type_id = evt.target.id() * -1;

        if (!tap_flag) {
            add_new_node_to_module(evt.target.position(), node_type_id)
        }
        tap_flag = false;
    });

    obj.on('tap', 'edge', function(evt){
        var edge = evt.target;
        // $('a[href="#moduleEdgeEdit"]').click();
        $('a[href="#edge-{0}"]'.format(edge.id())).click();
        $('#module-edge-detail-modal').modal('show');
    });

    obj.on('tap', function(event){
        var evtTarget = event.target;
        if (evtTarget === cy){
            $('a[href="#moduleNodeEdgeEmpty"]').click();
        }
    });
}

window.setInterval(function(){
    savePositionToNode(cy);
}, 5000);

function savePositionToNode(obj){
    var nodes = obj.elements('node[id > 0]'),
        positions = [],
        module_id = get_current_module_id();

    $.each(nodes, function(idx, node){
        //console.log(node.data('id'), node.position('x'), node.position('y'))
        positions.push({
            'node_id': node.data('id'),
            'posx': node.position('x'),
            'posy': node.position('y')
        });
    });

    var data = {
        'module_id': module_id,
        'positions': JSON.stringify(positions),
        'csrfmiddlewaretoken': '{{csrf_token}}'
    };
    //console.log(data)
    $.ajax({
        type: 'POST',
        data: data,
        url: '{% url "graphs:node_save_positions" %}',
        dataType: 'json'
    });
}

function get_current_module_id(){
    var url = window.location.href.split('/');

    return url[url.length - 2];
}

function module_view_options(){
    $('.dropdown-toggle').dropdown();
    $('#divNewNotifications li > a').click(function(){
    if (this.text !== ' View Options ') {
        if (this.text !== ' Failed Testcases ') {
            $('#text').text($(this).html());
        }
    }
    if (this.text === ' Default ') {
        $("#default").change();
    }
    if (this.text === ' Data Gaps ') {
        $("#data-gaps").change();
    }
    // if (this.text === ' Failed Testcases ') {
    //     $("#failed-testcases").change();
    // }
    $('#divNewNotifications li').css('background-color', 'white');
    });

    $('#data-gaps').change(function(){
        if (cy_edges_gap.length === 0) {
            cy_edges_gap = JSON.parse(JSON.stringify(cy_edges_default));
            $.each(cy_data_edges, function (key, value) {
                if (!$.isEmptyObject(value.tcs_cannot_route)) {
                    $.each(cy_edges_gap, function () {
                        if (this.data.id == value.id) {
                            this.data.color = '#FF3333';
                            return false
                        }
                    })
                }
            });
        }

        cy.elements().remove();
        cy = create_cy_object(cy_nodes_default, cy_edges_gap);
    });

    $('#default').change(function(){
        cy.elements().remove();
        cy = create_cy_object(cy_nodes_default, cy_edges_default);
    });
}

function add_new_node_to_module(pos, node_type_id) {
    // console.log(node_type_id)
    var node_new_modal = $('#module-node-new-modal'),
        positions = {
            'posx': pos.x,
            'posy': pos.y
        },
        options = node_new_modal.find('select[name="type"] option').clone();

    if (typeof node_type_id !== 'undefined'){
        var opts = options.filter(function (t) {
            return parseInt(this.value) === parseInt(node_type_id);
        });
        node_new_modal.find('select[name="type"]').html(opts);

        node_new_modal.find('select[name="type"]').val(node_type_id);
        var location = node_new_modal.find('#project-node-new-properties');
        load_keys_from_type_contents(node_type_id, location, 'node')
    }

    node_new_modal.find('input[name="positions"]').val(JSON.stringify(positions));
    node_new_modal.modal('show');
    node_new_modal.bind('hidden.bs.modal', function () {
        node_new_modal.find('select[name="type"]').html(options);
        cy.elements().remove();
        cy = create_cy_object(cy_nodes_default, cy_edges_default)
    })
}

function add_new_edge_to_module(pos) {
    // console.log('New Edge', pos)
    $('#module-edge-new-modal').modal('show')
}

function remove_node_from_module(node) {
    // console.log('Remove Node', node.data())
    var deleteModal = $('#nodeEdgeDeleteModal');

    deleteModal.find('input[name="nodeEdgeDeleteModuleId"]').val(get_current_module_id());
    deleteModal.find('input[name="nodeEdgeDeleteNodeId"]').val(node.data().id);
    deleteModal.find('input[name="nodeEdgeDeleteNodeName"]').val(node.data().label);
    deleteModal.find('input[name="nodeEdgeDeleteEdgeId"]').val('');
    deleteModal.find('input[name="nodeEdgeDeleteEdgeName"]').val('');

    deleteModal.modal('show')
}

function remove_edge_from_module(edge) {
    // console.log('Remove Edge', edge.data())
    var deleteModal = $('#nodeEdgeDeleteModal');

    deleteModal.find('input[name="nodeEdgeDeleteModuleId"]').val(get_current_module_id());
    deleteModal.find('input[name="nodeEdgeDeleteNodeId"]').val('');
    deleteModal.find('input[name="nodeEdgeDeleteNodeName"]').val('');
    deleteModal.find('input[name="nodeEdgeDeleteEdgeId"]').val(edge.data().id);
    deleteModal.find('input[name="nodeEdgeDeleteEdgeName"]').val(edge.data().name);

    deleteModal.modal('show')
}

function add_new_nodes_shape_to_graph(nodes) {
    var pos_x_initial = 20;

    var obj = [
        {
            'node_type': 'Start',
            'node_image': 'start',
            'node_id': '-1'
        },
        {
            'node_type': 'PlayPrompt',
            'node_image': 'say_',
            'node_id': '-2'
        },
        {
            'node_type': 'MenuPrompt',
            'node_image': 'prompt_',
            'node_id': '-3'
        },
        {
            'node_type': 'MenuPromptConfirm',
            'node_image': 'prompt_with_confirm_',
            'node_id': '-4'
        },
        {
            'node_type': 'DataQueriesDatabase',
            'node_image': 'database',
            'node_id': '-6'
        },
        {
            'node_type': 'Transfer',
            'node_image': 'transfer',
            'node_id': '-10'
        },
        {
            'node_type': 'LanguageSelect',
            'node_image': 'language_select',
            'node_id': '-13'
        },
        {
            'node_type': 'SetVariable',
            'node_image': 'set_variable',
            'node_id': '-14'
        },
        {
            'node_type': 'DecisionCheck',
            'node_image': 'decision_check',
            'node_id': '-15'
        }
    ];

    $.each(obj, function (idx, item) {
        nodes.push({
            'data': {
                'id': item['node_id'],
                'label': item['node_type'],
                'image': image_url +'mdta-shapes/{0}.png'.format(item['node_image']),
                'color': 'white'
            },
            'renderedPosition': {
                x: pos_x_initial + idx * 80,
                y: graph_height - 30
            }
        })
    });

    return nodes;
}

function module_qtip_event(obj) {
    obj.elements('node[id < 0]').qtip({
        content: function(){ return 'Drag to Add New ' + this.data().label + ' Node' },
        position: {
            my: 'top center',
            at: 'bottom center'
        },
        style: {
            classes: 'qtip-bootstrap',
            tip: {
                width: 16,
                height: 8
            }
        }
    })
}