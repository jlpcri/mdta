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
    var options = {
        nodes: {
            shape: 'ellipse',
            //fontSize: 10
        },
        edges: {
            //style: 'arrow',
            color: '#000',
            length: 190,
            arrows: 'to'
        },
        width: '100%',
        height: '800px'
    };

    // initialize your network!
    var network = new vis.Network(container, data, options);
}

$(document).ready(function(){
    draw_project_graph();
});