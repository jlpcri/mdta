/**
 * Created by sliu on 5/5/16.
 */
console.log('aaa')
$('.editProject').on('show.bs.modal', function(e){
    console.log('BBBB')
    var id = $(e.relatedTarget).data('project-id'),
        name = $(e.relatedTarget).data('project-name');
        lead = $(e.relatedTarget).data('project-lead'),
        worker = $(e.relatedTarget).data('project-worker');

    $(e.currentTarget).find('input[name="editProjectId"]').val(id);
    $(e.currentTarget).find('input[name="editProjectName"]').val(name);

});