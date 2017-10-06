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
            'shape': value['shape'],
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
        fit: true
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
            'color': '#00134d'
        }
    })
});

var cy = create_cy_object(cy_nodes_default, cy_edges_default);

function create_cy_object(cy_nodes, cy_edges) {
    var obj = cytoscape({
        container: $('#node_in_module_cy')[0],
        elements: {
            nodes: cy_nodes,
            edges: cy_edges
        },
        style: [
            {
                selector: 'node',
                style: {
                    'background-color': 'data(color)',
                    'label': 'data(label)'
                }
            },
            {
                selector: 'node[shape="box"]',
                style: {
                    'text-valign': 'center',
                    'width': '110%',
                    'shape': 'roundrectangle'
                }
            },
            {
                selector: 'node[shape="star"]',
                style: {
                    'width': '40%',
                    'height': '40%',
                    'shape': 'star'
                }
            },
            {
                selector: 'node[shape="ellipse"]',
                style: {
                    //'font-family': 'Gill Sans Extrabold, sans-serif',
                    'width': '110%',
                    'shape': 'ellipse'
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
                selector: 'node:selected',
                style: {
                    'background-color': '#ccd9ff'
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
        userZoomingEnabled: false,
        boxSelectionEnabled: true
    });

    module_context_menu(obj);
    module_click_event(obj);

    return obj;
}

module_view_options();

function module_context_menu(cy){
    cy.contextMenus({
        menuItems: [
            {
                id: 'verbiages',
                content: 'Verbiages',
                tooltipText: 'Prompt Verbiages',
                selector: 'node',
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
                id: 'remove',
                content: 'Remove',
                tooltipText: 'Remove Node',
                selector: 'node',
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
                id: 'remove',
                content: 'Remove',
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

function module_click_event(cy){
    cy.on('tap', 'node', function(evt){
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

    cy.on('tapend', 'node', function (evt) {
        var node = evt.target;

        // console.log(node.position())
        var data = {
            'node_id': node.id(),
            'position': node.position()
        };
        sendMessage(JSON.stringify(data))
    });

    cy.on('tap', 'edge', function(evt){
        var edge = evt.target;
        // $('a[href="#moduleEdgeEdit"]').click();
        $('a[href="#edge-{0}"]'.format(edge.id())).click();
        $('#module-edge-detail-modal').modal('show');
    });

    cy.on('tap', function(event){
        var evtTarget = event.target;
        if (evtTarget === cy){
            $('a[href="#moduleNodeEdgeEmpty"]').click();
        }
    });
}

window.setInterval(function(){
    savePositionToNode(cy);
}, 5000);

//$(window).bind('beforeunload', function(){
//    savePositionToNode(cy);
//});

function savePositionToNode(cy){
    var nodes = cy.nodes(),
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

function add_new_node_to_module(pos) {
    // console.log('New Node', pos)
    $('#module-node-new-modal').modal('show')
}

function add_new_edge_to_module(pos) {
    // console.log('New Edge', pos)
    $('#module-edge-new-modal').modal('show')
}

function remove_node_from_module(node) {
    console.log('Remove Node', node.data().id)
}

function remove_edge_from_module(edge) {
    console.log('Remove Edge', edge.data().id)
}