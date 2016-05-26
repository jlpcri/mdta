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

$('.newModule form').on('submit', function(){
    var name = $('.newModule form #id_name').val(),
        project = $('.newModule form #id_project').val();

    if (name == ''){
        showErrMsg('#newModuleErrMessage', 'Name is Empty');
        return false;
    }
    if (project == ''){
        showErrMsg('#newModuleErrMessage', 'Project is Empty');
        return false;
    }
});

$('.editModule').on('show.bs.modal', function(e){
    var id = $(e.relatedTarget).data('module-id'),
        project = $(e.relatedTarget).data('module-project'),
        name = $(e.relatedTarget).data('module-name');

    $(e.currentTarget).find('input[name="editModuleId"]').val(id);
    $(e.currentTarget).find('input[name="editModuleName"]').val(name);
    $('#editModuleProject').val(project);
});

$('.editModule form').on('submit', function(){
    var name = $('#editModuleName').val();

    if (name == ''){
        showErrMsg('#editModuleErrMessage', 'Name is Empty');
        return false;
    }
});