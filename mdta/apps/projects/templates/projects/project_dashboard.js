/**
 * Created by sliu on 10/14/16.
 */
$('.editTestHeader').on('show.bs.modal', function(e){
    var testheader_id = $(e.relatedTarget).data('testheader-id'),
        testheader_name = $(e.relatedTarget).data('testheader-name');

    $(e.currentTarget).find('input[name="editTestHeaderId"]').val(testheader_id);
    $(e.currentTarget).find('input[name="editTestHeaderName"]').val(testheader_name);
});