/**
 * Created by sliu on 8/9/17.
 */

var cy_nodes = [],
    cy_edges = [],
    cy_layout_options = '',
    cy_layout_flag = true;  // all modules have positions

$.each(cy_data_nodes, function(key, value){
    var posx = 0,
        posy = 0;
    if (!value['positions']){
        if (cy_layout_flag){
            cy_layout_flag = false
        }
    } else {
        posx = value['positions']['posx'];
        posy = value['positions']['posy']
    }
    cy_nodes.push({
        'data': {
            'id': value['id'],
            'label': value['label']
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
        fit: true,
        padding: 30
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
    cy_edges.push({
        'data': {
            'id': value['id'],
            'source': value['from'],
            'target': value['to'],
            'label': value['label']
        }
    })
});
//console.log(cy_nodes, cy_edges)
var cy = cytoscape({
    container: $('#module_in_project_cy')[0],
    elements: {
        nodes: cy_nodes,
        edges: cy_edges
    },
    style:[
        {
            selector: 'node',
            style: {
                'background-image': image_url + 'blue-infrastructure-graphics_11435264594_o.png',
                'background-fit': 'contain',
                'background-clip': 'node',
                'label': 'data(label)',
                'text-valign': 'bottom'
            }
        },
        {
            selector: 'edge',
            style: {
                'width': 1,
                'line-color': '#00134d',
                'curve-style': 'bezier',
                'target-arrow-color': '#00134d',
                'target-arrow-shape': 'triangle',
                'label': 'data(label)'
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
    zoomingEnabled: true
});

$(window).bind('beforeunload', function () {
    savePositionToModule(cy);
});

cy_click_event(cy);

function savePositionToModule(cy){
    var nodes = cy.nodes(),
        positions = [];

    $.each(nodes, function(idx, node){
        positions.push({
            'module_id': node.data('id'),
            'posx': node.position('x'),
            'posy': node.position('y')
        });
    });
    var data = {
        'positions': JSON.stringify(positions),
        'csrfmiddlewaretoken': '{{csrf_token}}'
    };
    $.ajax({
        type: 'POST',
        data: data,
        url: '{%url "graphs:node_save_positions"%}?type=module',
        dataType: 'json'
    })
}

function cy_click_event(cy){
    cy.on('tap', 'node', function(evt){
        var base_url = '',
            tmp = window.location.href.split('/'),
            module = evt.target;
        for (var i = 0; i < tmp.length -3; i++){
            base_url += tmp[i] + '/'
        }
        window.location.href = base_url + 'project_module_detail/' + module.id();
    });

    cy.on('tap', 'edge', function(evt){
        var edge = evt.target;

        $('a[href="#projectEdges"]').click();
        $('a[href="#project-edge-{0}"]'.format(edge.id())).click();
        $('.edges-between-modules').show();
        $('.edges-between-modules-contents').hide();
    });

    cy.on('tap', function(evt){
        var evtTarget = evt.target;
        if(evtTarget === cy){
            $('a[href="#projectModules"]').click();
        }
    })
}