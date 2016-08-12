/**
 * Created by sliu on 8/10/16.
 */

$(document).ready(function () {
    $('#tc-subnav-tabs').find('a[href="#tc-projects"]').tab('show');

    if ('{{link_id}}') {
        $('a[href="#project-{0}"]'.format('{{link_id}}')).click();
    }
});