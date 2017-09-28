/**
 * Created by sliu on 8/9/17.
 */

var cy_nodes_default = [],
    cy_nodes_gap = [],
    cy_edges_default = [],
    image_default = image_url + 'blue-infrastructure-graphics_11435264594_o.png',
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
    cy_nodes_default.push({
        'data': {
            'id': value['id'],
            'label': value['label'],
            'image': image_default
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
    cy_edges_default.push({
        'data': {
            'id': value['id'],
            'source': value['from'],
            'target': value['to'],
            'label': value['label']
        }
    })
});
//console.log(cy_nodes, cy_edges_default)

var cy = create_cy_object(cy_nodes_default, cy_edges_default);

function create_cy_object(cy_nodes, cy_edges) {
    var obj = cytoscape({
        container: $('#module_in_project_cy')[0],
        elements: {
            nodes: cy_nodes,
            edges: cy_edges
        },
        style: [
            {
                selector: 'node',
                style: {
                    'background-image': 'data(image)',
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
        userZoomingEnabled: false
    });

    project_context_menu(obj);
    project_click_event(obj);

    return obj;
}

project_view_options();

window.setInterval(function(){
    savePositionToModule(cy);
}, 5000);

//$(window).bind('beforeunload', function () {
//    savePositionToModule(cy);
//});


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

function project_context_menu(cy){
    cy.contextMenus({
        menuItems: [
            {
                id: 'rename',
                content: 'Rename',
                tooltipText: 'Rename Module',
                selector: 'node',
                onClickFunction: function (event) {
                    var target = event.target.data(),
                        module_edit = $('#module-edit-modal');

                    module_edit.find('input[name="editModuleId"]').val(target['id']);
                    module_edit.find('input[name="editModuleName"]').val(target['label']);
                    module_edit.find('.modal-title').html('Module Edit/Delete');
                    module_edit.modal('show')
                },
                hasTrailingDivider: true
            },
            /*
            {
                id: 'remove',
                content: 'Remove',
                tooltipText: 'Remove Module',
                selector: 'node',
                onClickFunction: function (event) {
                    var target = event.target || event.cyTarget;
                    console.log('Remove module', target.id())
                    },
                hasTrailingDivider: true
            },

            {
                id: 'add-node',
                content: 'New Module',
                tooltipText: 'Add New Module',
                coreAsWell: true,
                onClickFunction: function (event) {
                    var target = event.target;
                    console.log('Add module', target)
                }
            }
            */
        ]
    });
}

function project_click_event(cy){
    cy.on('tap', 'node', function(evt){
        var base_url = '',
            tmp = window.location.href.split('/'),
            module = evt.target;
        for (var i = 0; i < tmp.length -3; i++){
            base_url += tmp[i] + '/'
        }
        window.location.href = base_url + 'project_module_detail/' + module.id();
    });

    cy.on('free', 'node', function (evt) {
        var node = evt.target;
        var data = {
            'node_id': node.id(),
            'position': node.position()
        };
        sendMessage(JSON.stringify(data))
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
    });

    // cy.on('cxttapend', 'node', function (evt) {
    //     var module = evt.target;
    //     console.log('Popup Module Detail', window.screen.availHeight)
    // })


}

function project_view_options(){
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

    // var flag = false;
    $('#data-gaps').change(function(){
        var flag = false;

        if (cy_nodes_gap.length === 0) {
            cy_nodes_gap = JSON.parse(JSON.stringify(cy_nodes_default));

            $.each(cy_data_nodes, function (key, value) {
                if (!$.isEmptyObject(value.data)) {
                    $.each(value.data, function (subk, subv) {
                        if (!$.isEmptyObject(subv.tcs_cannot_route)) {
                            //console.log(value.id, subv)
                            $.each(cy_nodes_gap, function () {
                                if (this.data.id == value.id) {
                                    this.data.image = image_url + 'yellow-infrastructure-graphics_o.png'
                                    flag = true;
                                    return false
                                }
                            });

                            if (flag) {
                                return false
                            }
                        }
                    })
                } else {
                    $.each(cy_nodes_gap, function () {
                        if (this.data.id == value.id) {
                            this.data.image = image_url + 'red-infrastructure-graphics_o.png'
                        }
                    })
                }
            });
        }

        cy.elements().remove();
        cy = create_cy_object(cy_nodes_gap, cy_edges_default);
    });

    $('#default').change(function(){
        cy.elements().remove();
        cy = create_cy_object(cy_nodes_default, cy_edges_default);
    });
}