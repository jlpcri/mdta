/**
 * Created by sliu on 8/9/17.
 */

var cy_nodes_default = [],
    cy_nodes_gap = [],
    cy_edges_default = [],
    image_default = image_url + 'blue-infrastructure-graphics_11435264594_o.png',
    image_start = image_url + 'west-ivr-graphic_11435724503_o.png',
    image_new = image_url + 'green-infrastructure-graphics_11435449795_o.png',
    cy_layout_options = '',
    cy_layout_flag = true;  // all modules have positions

$.each(cy_data_nodes, function(key, value){
    var posx = 0,
        posy = 0,
        image = '';

    if (!value['positions']){
        if (cy_layout_flag){
            cy_layout_flag = false
        }
    } else {
        posx = value['positions']['posx'];
        posy = value['positions']['posy']
    }
    if (value['start_module'] === true) {
        image = image_start
    } else {
        image = image_default
    }

    cy_nodes_default.push({
        'data': {
            'id': value['id'],
            'label': value['label'],
            'image': image
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
        fit: false,
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
    // cy_nodes.push({
    //     'data': {
    //         'id': -1,
    //         // 'label': 'New Module',
    //         'image': image_new
    //     },
    //     'renderedPosition': {
    //         x: 100,
    //         y: graph_height - 30
    //     }
    // });
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
                    // 'shape': 'rectangle',
                    // 'height': '40px',
                    // 'width': '40px',
                    'label': 'data(label)',
                    'text-valign': 'bottom'
                }
            },
            // {
            //     selector: 'node[id < 0]',
            //     style: {
            //         'text-valign': 'bottom',
            //         'font-size': '12'
            //     }
            // },
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
        userZoomingEnabled: true
    });

    // project_draw_fixed_eles(obj);

    project_context_menu(obj);
    project_click_event(obj);
    // project_qtip_event(obj);

    return obj;
}

project_view_options();

var save_modules_location = window.setInterval("savePositionToModule(cy)", 5000);

if ('{{ project.testrail }}' === 'None') {
    var is_project_has_testrail = window.setInterval("check_project_has_testrail()", 5000 * 60 * 60);  // 1 hour 5000 * 60 * 60
} else {
    window.clearInterval(is_project_has_testrail);
}
if ('{{ project.test_header }}' === 'None'){
    var is_project_has_testheader = window.setInterval("check_project_has_testheader()", 5000 * 60 * 60 * 2); // 2 hours 5000 * 60 * 60 * 2
} else {
    window.clearInterval(is_project_has_testheader);
}

function savePositionToModule(cy){
    var nodes = cy.elements('node'),
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
                selector: 'node[id > 0]',
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
            */
            {
                id: 'new-module',
                content: 'New Module',
                tooltipText: 'Add New Module',
                coreAsWell: true,
                onClickFunction: function (event) {
                    add_new_module(event.position);
                }
            }
        ]
    });
}

function add_new_module(pos) {
    var module_new = $('#module-new-modal');
    var position = {
            'posx': pos.x,
            'posy': pos.y
        };

    module_new.find('input[name="positions"]').val(JSON.stringify(position));
    module_new.modal('show');
    // module_new.bind('hidden.bs.modal', function () {
    //     cy.elements().remove();
    //     cy = create_cy_object(cy_nodes_default, cy_edges_default);
    //
    // })
}

function project_click_event(cy){
    // var tap_flag = false;

    cy.on('tap', 'node[id > 0]', function(evt){
        var base_url = '',
            tmp = window.location.href.split('/'),
            module = evt.target;
        for (var i = 0; i < tmp.length -3; i++){
            base_url += tmp[i] + '/'
        }
        window.location.href = base_url + 'project_module_detail/' + module.id();
    });

    cy.on('free', 'node[id > 0]', function (evt) {
        var node = evt.target;
        var data = {
            'node_id': node.id(),
            'position': node.position(),
            'node_data': node.data()
        };
        sendMessage(JSON.stringify(data))
    });

    // cy.on('tap', 'node[id < 0]', function (evt) {
    //     tap_flag = true;
    // });
    //
    // cy.on('free', 'node[id < 0]', function (evt) {
    //     if (!tap_flag) {
    //         add_new_module(evt.target.position())
    //     }
    //     tap_flag = false;
    // });

    cy.on('tap', 'edge', function(evt){
        var edge = evt.target;

        $('#edges-between-modules-modal').modal('show');
        $('a[href="#project-edge-{0}"]'.format(edge.id())).click();
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

function project_draw_fixed_eles(obj) {
    var bottomLayer = obj.cyCanvas({
            zIndex: -1
        }),
        canvas = bottomLayer.getCanvas(),
        ctx = canvas.getContext('2d');

    obj.on('render cyCanvas.resize', function (evt) {

        bottomLayer.resetTransform(ctx);
        ctx.save();
        ctx.font = "24px Helvetica";
        ctx.fillStyle = "red";
        ctx.fillText("This text is fixed", 200, graph_height);

        // ctx.drawImage(image_new, 100, graph_height)
        ctx.restore()
    })
}

function project_qtip_event(obj) {
    obj.elements('node[id < 0]').qtip({
        content: function(){ return 'Drag to Add New Module' },
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

function check_project_has_testheader() {
    // console.log('testheader', project_id)
    $.getJSON("{% url 'graphs:check_object_has_tr_th' %}?choice={0}&project_id={1}".format('testheader', project_id)).done(function (data) {
        if (data['message'].length > 0) {
            $('#notifyTestHeaderModal').modal('show');
        }
    })
}

function check_project_has_testrail() {
    // console.log('testrail', project_id)
    $.getJSON("{% url 'graphs:check_object_has_tr_th' %}?choice={0}&project_id={1}".format('testrail', project_id)).done(function (data) {
        if (data['message'].length > 0) {
            $('#notifyTestRailModal').modal('show');
        }
    })
}