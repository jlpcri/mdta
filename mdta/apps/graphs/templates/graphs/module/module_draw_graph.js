/**
 * Created by sliu on 8/3/17.
 */
var cy_nodes = [],
    cy_edges = [];
$.each(cy_data_nodes, function(key, value){
    //console.log(key, value)
    var posx = 0,
        posy = 0;
    if (!value['positions']){
        posx = key * 100;
        posy = key * 100
    } else{
        posx = value['positions']['posx'];
        posy = value['positions']['posy']
    }

    cy_nodes.push({
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

$.each(cy_data_edges, function(key, value){
    //console.log(value),
    cy_edges.push({
        'data': {
            'id': value['id'],
            'source': value['from'],
            'target': value['to']
        }
    })
});

var cy = cytoscape({
    container: $('#module_graph_cy')[0],
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
                'font-family': 'Gill Sans Extrabold, sans-serif',
                'width': '110%',
                'shape': 'ellipse'
            }
        },
        {
            selector: 'edge',
            style: {
                'width': 1,
                'line-color': '#00134d',
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
    layout: {
        name: 'preset',
        //rows: 1
    },
    zoomingEnabled: false,
    boxSelectionEnabled: true
});

cy_click_event(cy);
function cy_click_event(cy){
    cy.on('tap', 'node', function(evt){
        var node = evt.target;
        $.getJSON("{% url 'graphs:get_module_id_from_node_id'%}?node_id={0}".format(node.id())).done(function(data){
            var current_module_id = get_current_module_id();

            if (data['module_id'] == current_module_id){
                $('#select_node_id').val(node.id())
            } else {
                $('#select_node_id').val('-1')
            }
        });
        $('a[href="#moduleNodeEdit"]').click();
        $('a[href="#node-{0}"]'.format(node.id())).click();
    });

    cy.on('tap', 'edge', function(evt){
        var edge = evt.target;
        $('a[href="#moduleEdgeEdit"]').click();
        $('a[href="#edge-{0}"]'.format(edge.id())).click();
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
}, 5000 * 12 * 20);

$(window).bind('beforeunload', function(){
    savePositionToNode(cy);
});

function savePositionToNode(cy){
    var nodes = cy.nodes(),
        positions = [],
        module_id = get_current_module_id();

    $.each(nodes, function(idx, node){
        //console.log(node.data('id'), node.position('x'), node.position('y'))
        positions.push({
            'node_id': node.data('id'),
            'posx': parseFloat(node.position('x')).toFixed(2),
            'posy': parseFloat(node.position('y')).toFixed(2)
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