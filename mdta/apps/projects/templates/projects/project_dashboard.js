/**
 * Created by sliu on 10/14/16.
 */
$('.editTestHeader').on('show.bs.modal', function(e){
    var testheader_id = $(e.relatedTarget).data('testheader-id'),
        testheader_name = $(e.relatedTarget).data('testheader-name');

    $(e.currentTarget).find('input[name="editTestHeaderId"]').val(testheader_id);
    $(e.currentTarget).find('input[name="editTestHeaderName"]').val(testheader_name);
});

function deleteTestrailModal (project_name, project_id) {
    $('#deleteTitle').text('Delete TestRail Configuration: \"' + project_name + '\" ?');
    $('#deleteTestRailButton').attr('href', '/mdta/testcases/testrail_configuration_delete/' + project_id);

    $('#confirmModal').modal('show');
}

$(document).ready(function(){
    if (last_tab){
        $('#subnav-tabs').find('a[href="#{0}"]'.format(last_tab)).tab('show');
    } else {
        $('#subnav-tabs').find('a[href="#project"]').tab('show');
    }
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
        node_type_keys = $(e.relatedTarget).data('node-type-keys'),
        node_type_subkeys = $(e.relatedTarget).data('node-type-subkeys'),
        node_type_verbiagekeys = $(e.relatedTarget).data('node-type-verbiagekeys');

    $(e.currentTarget).find('input[name="editNodeTypeId"]').val(node_type_id);
    $(e.currentTarget).find('input[name="editNodeTypeName"]').val(node_type_name);
    $(e.currentTarget).find('input[name="editNodeTypeKeys"]').val(node_type_keys);
    $(e.currentTarget).find('input[name="editNodeTypeSubKeys"]').val(node_type_subkeys);
    $(e.currentTarget).find('input[name="editNodeTypeVerbiageKeys"]').val(node_type_verbiagekeys);

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
        edge_type_keys = $(e.relatedTarget).data('edge-type-keys'),
        edge_type_subkeys = $(e.relatedTarget).data('edge-type-subkeys');

    $(e.currentTarget).find('input[name="editEdgeTypeId"]').val(edge_type_id);
    $(e.currentTarget).find('input[name="editEdgeTypeName"]').val(edge_type_name);
    $(e.currentTarget).find('input[name="editEdgeTypeKeys"]').val(edge_type_keys);
    $(e.currentTarget).find('input[name="editEdgeTypeSubKeys"]').val(edge_type_subkeys);

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

$('.editLanguage').on('show.bs.modal', function(e){
    var language_id = $(e.relatedTarget).data('language-id'),
        project_id = $(e.relatedTarget).data('language-project-id'),
        name = $(e.relatedTarget).data('language-name'),
        root_path = $(e.relatedTarget).data('language-rootpath');

    $(e.currentTarget).find('input[name="editLanguageId"]').val(language_id);
    $(e.currentTarget).find('select').val(project_id);
    $(e.currentTarget).find('input[name="editLanguageName"]').val(name);
    $(e.currentTarget).find('input[name="editLanguageRootPath"]').val(root_path);
});
