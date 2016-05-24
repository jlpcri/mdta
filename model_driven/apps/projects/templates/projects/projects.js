/**
 * Created by sliu on 5/5/16.
 */
$('.newProject form').on('submit', function(){
    var name = $('.newProject form #id_name').val();

    if (name == ''){
        showErrMsg('#newProjectErrMessage', 'Name is Empty');
        return false;
    }
});

$('.editProject').on('show.bs.modal', function(e){
    var id = $(e.relatedTarget).data('project-id'),
        name = $(e.relatedTarget).data('project-name'),
        lead = $(e.relatedTarget).data('project-lead');

    $(e.currentTarget).find('input[name="editProjectId"]').val(id);
    $(e.currentTarget).find('input[name="editProjectName"]').val(name);
    $('#editProjectLead').val(lead);

    $.getJSON("{% url 'projects:fetch_project_members'%}?id={0}".format(id)).done(function(data){
        $('#editProjectMembers').val(data);
    });

});

$('.editProject form').on('submit', function(){
    var name = $('#editProjectName').val();

    if (name == ''){
        showErrMsg('#editProjectErrMessage', 'Name is Empty');
        return false;
    }
});