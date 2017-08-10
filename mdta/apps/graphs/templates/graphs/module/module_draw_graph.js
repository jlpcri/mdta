/**
 * Created by sliu on 8/3/17.
 */
var cy_nodes = [],
    cy_edges = [],
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
    cy_edges.push({
        'data': {
            'id': value['id'],
            'source': value['from'],
            'target': value['to']
        }
    })
});

var cy = cytoscape({
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
                'label': 'data(label)',
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
    layout: cy_layout_options,
    zoomingEnabled: true,
    boxSelectionEnabled: true
});

cy_click_event(cy);
cy_double_click_event(cy);
view_options();

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

function cy_double_click_event(cy){
    var tappedBefore,
        tappedTimeout;

    cy.on('tap', function(event){
        var tappedNow = event.target;
        if (tappedTimeout && tappedBefore){
            clearTimeout(tappedTimeout);
        }
        if (tappedBefore === tappedNow){
            tappedNow.trigger('doubleTap');
            tappedBefore = null;
        } else {
            tappedTimeout = setTimeout(function(){
                tappedBefore = null;
            }, 300);
            tappedBefore = tappedNow;
        }
    });

    cy.on('doubleTap', 'node', function (event) {
        var node = event.target;

        $.getJSON("{% url 'graphs:get_module_id_from_node_id' %}?node_id={0}".format(node.id())).done(function(data){
            var base_url = '',
                tmp = window.location.href.split('/'),
                current_module_id = tmp[tmp.length - 2];

            for (var i = 0; i < tmp.length - 2; i++) {
                base_url += tmp[i] + '/'
            }
            if(!(data['module_id'] == current_module_id)){
                window.location.href = base_url + data['module_id'];
                $('body').css('cursor', 'progress');
            } else {
                open_prompts_modal(data['node_data'], node.id());
            }
        })
    })
}

//window.setInterval(function(){
//    savePositionToNode(cy);
//}, 5000 * 12 * 20);

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

function view_options(){
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
        var n = JSON.stringify("{{ network_edges|escapejs }}");
        var edge = JSON.parse(n);
        $.each(JSON.parse(edge), function(idx, obj) {
            console.log(obj)
            if (!$.isEmptyObject(obj.tcs_cannot_route)) {
                var route = obj.tcs_cannot_route;
                var id = obj.id;
                for (var i = 0; i < route.length; ++i) {
                    for (var ind in route[i]) {
                        edges.update([{id: id, color: '#FF3333'}]);
                    }
                }
            }
            else {
                $('a[href="#moduleNodeEdgeEmpty"]').click();
            }
        });
    });

    $('#default').change(function(){
        var n = JSON.stringify("{{ network_edges|escapejs }}");
        var edge = JSON.parse(n);
        $.each(JSON.parse(edge), function(idx, obj) {
            var id = obj.id;
            edges.update([{id: id, color: '#000'}]);
        });
    });
}