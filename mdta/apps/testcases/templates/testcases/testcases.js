/**
 * Created by sliu on 8/10/16.
 */

$(document).ready(function () {
    $('#tc-subnav-tabs').find('a[href="#tc-projects"]').tab('show');

    if ('{{link_id}}') {
        $('a[href="#project-{0}"]'.format('{{link_id}}')).click();
    }
});

function deleteModal (project_name, project_id) {
    $('#deleteTitle').text('Delete TestRail Configuration: \"' + project_name + '\" ?');
    $('#deleteTestRailButton').attr('href', '/mdta/testcases/testrail_configuration_delete/' + project_id);

    $('#confirmModal').modal('show');
}