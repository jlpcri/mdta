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