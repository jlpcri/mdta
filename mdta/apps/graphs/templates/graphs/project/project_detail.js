/**
 * Created by sliu on 6/7/16.
 */

$('.editModule').on('show.bs.modal', function(e){
    var module_id = $(e.relatedTarget).data('module-id'),
        module_name = $(e.relatedTarget).data('module-name');

    $(e.currentTarget).find('input[name="editModuleId"]').val(module_id);
    $(e.currentTarget).find('input[name="editModuleName"]').val(module_name);
    $('.editModule .modal-title').html('Module Edit/Delete');
});

$('.editModule form').on('submit', function(){
    var module_name = $('#editModuleName').val();

    if (module_name == ''){
        showErrMsg('#editModuleErrMessage', 'Name is Empty');
        return false;
    }
});

$('.projectEdgeEditForm #projectEdgeEditType').on('change', function(){
    var edge_type_id = $(this).find('option:selected').val(),
        location = $(this).closest('.projectEdgeEditForm').find('#project-edge-edit-properties');

    load_keys_from_type_contents(edge_type_id, location, 'edge')
});

function draw_project_graph() {
    //// create an array with nodes
    //var nodes = new vis.DataSet([
    //    {id: 1, label: 'Node 1'},
    //    {id: 2, label: 'Node 2'},
    //    {id: 3, label: 'Node 3'},
    //    {id: 4, label: 'Node 4'},
    //    {id: 5, label: 'Node 5'}
    //]);
    //
    //// create an array with edges
    //var edges = new vis.DataSet([
    //    {from: 1, to: 3},
    //    {from: 1, to: 2},
    //    {from: 2, to: 4},
    //    {from: 2, to: 5}
    //]);

    // create a network
    var container = document.getElementById('module_in_project');

    // provide the data in the vis format
    var data = {
        nodes: nodes,
        edges: edges
    };
    var image_url = 'http://apps.qaci01.wic.west.com/static/common/brand_icons/turnpost-png-graphics/';
    var options = {
        nodes: {
            shape: 'image',
            image: image_url + 'blue-infrastructure-graphics_11435264594_o.png',
            //image: image_url + 'west-ivr-graphic_11435724503_o.png',
            size: 25
        },
        edges: {
            color: '#000',
            length: 190,
            arrows: 'to',
            arrowStrikethrough: false
        },
        width: '100%',
        height: '800px'
    };

    // initialize your network!
    var network = new vis.Network(container, data, options);

    network.on('click', function(params){
        //console.log(params.nodes)
        if (!$.isEmptyObject(params.nodes)) {
            var current = '',
                tmp = window.location.href.split('/');
            for (var i = 0; i < tmp.length - 3; i++) {
                current += tmp[i] + '/'
            }
            $('#module_in_project').css('cursor', 'progress');
            window.location.href = current + 'project_module_detail/' + params.nodes;

        } else if (!$.isEmptyObject(params.edges)){
            //console.log(params.edges)
            $('a[href="#projectEdges"]').click();
            $('a[href="#project-edge-{0}"]'.format(params.edges)).click();
            $('.edges-between-modules').show();
            $('.edges-between-modules-contents').hide();
        } else {
            $('a[href="#projectModules"]').click();
        }
    })
}

$(document).ready(function(){
    $('a[href="#projectModules"]').click();
    draw_project_graph();
});

$('.list-group-item').click(function(){
    $('.edges-between-modules').hide();
    $('.edges-between-modules-contents').show();
});

$('.back-to-edges-between-modules').click(function(){
    $('.edges-between-modules').show();
    $('.edges-between-modules-contents').hide();
    $('a[href="#{0}"]'.format(this.value)).click();

});


$(document).on('change', ':file', function () {
    var input = $(this),
        numFiles = input.get(0).files ? input.get(0).files.length : 1,
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselect', [numFiles, label]);
});

$(document).ready(function () {
    $(':file').on('fileselect', function (event, numFiles, label) {

        var input = $(this).parents('.input-group').find(':text'),
            log = numFiles > 1 ? numFiles + ' files selected' : label;

        if (input.length) {
            input.val(log);
        } else {
            if (log) alert(log);
        }

    });
});
