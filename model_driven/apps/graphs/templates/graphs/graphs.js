/**
 * Created by sliu on 5/12/16.
 */


$(document).ready(function(){
    $('#subnav-tabs').find('a[href="#projects"]').tab('show');
});

$('.newNodeType form').on('submit', function(){
    var name = $('.newNodeType form #id_name').val();

    if (name == ''){
        showErrMsg('#newNodeTypeErrMessage', 'Name is Empty');
        return false;
    }
});

$('.editNodeType').on('show.bs.modal', function(e){
    var node_type_id = $(e.relatedTarget).data('node-type-id'),
        node_type_name = $(e.relatedTarget).data('node-type-name'),
        node_type_keys = $(e.relatedTarget).data('node-type-keys');

    $(e.currentTarget).find('input[name="editNodeTypeId"]').val(node_type_id);
    $(e.currentTarget).find('input[name="editNodeTypeName"]').val(node_type_name);
    $(e.currentTarget).find('input[name="editNodeTypeKeys"]').val(node_type_keys);

    $('.editNodeType .modal-title').html('Node Type Edit - ' + node_type_name);
    $('#editNodeTypeErrMessage').html('');
});

$('.editNodeType form').on('submit', function(){
    var name = $('#editNodeTypeName').val();

    if (name == ''){
        showErrMsg('#editNodeTypeErrMessage', 'Name is Empty');
        return false;
    }
});

$('.newEdgeType form').on('submit', function(){
    var name = $('.newEdgeType form #id_name').val();

    if (name == ''){
        showErrMsg('#newEdgeTypeErrMessage', 'Name is Empty');
        return false;
    }
});

$('.editEdgeType').on('show.bs.modal', function(e){
    var edge_type_id = $(e.relatedTarget).data('edge-type-id'),
        edge_type_name = $(e.relatedTarget).data('edge-type-name'),
        edge_type_keys = $(e.relatedTarget).data('edge-type-keys');

    $(e.currentTarget).find('input[name="editEdgeTypeId"]').val(edge_type_id);
    $(e.currentTarget).find('input[name="editEdgeTypeName"]').val(edge_type_name);
    $(e.currentTarget).find('input[name="editEdgeTypeKeys"]').val(edge_type_keys);

    $('.editEdgeType .modal-title').html('Edge Type Edit - ' + edge_type_name);
    $('#editEdgeTypeErrMessage').html('');
});

$('.editEdgeType form').on('submit', function(){
    var name = $('#editEdgeTypeName').val();

    if (name == ''){
        showErrMsg('#editEdgeTypeErrMessage', 'Name is Empty');
        return false;
    }
});

