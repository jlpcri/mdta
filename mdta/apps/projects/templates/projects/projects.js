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
        testrail = $(e.relatedTarget).data('project-testrail'),
        lead = $(e.relatedTarget).data('project-lead');

    $(e.currentTarget).find('input[name="editProjectId"]').val(id);
    $(e.currentTarget).find('input[name="editProjectName"]').val(name);
    $('#editProjectTestrail').val(testrail);
    $('#editProjectLead').val(lead);

    $.getJSON("{% url 'projects:fetch_project_catalogs_members'%}?id={0}&level=project".format(id)).done(function(data){
        $('#editProjectCatalogs').val(data['catalogs']);
        $('#editProjectMembers').val(data['members']);
    });

});

$('.editProject form').on('submit', function(){
    var name = $('#editProjectName').val();

    if (name == ''){
        showErrMsg('#editProjectErrMessage', 'Name is Empty');
        return false;
    }
});

$('.newModule').on('show.bs.modal', function(){
    var project_id = $('#id_project').val(),
        location = $('.newModule #id_catalog');

    set_catalog_selection_value(project_id, location);
});

$('.newModule #id_project').on('change', function(){
    var project_id = $(this).val(),
        location = $('.newModule #id_catalog');

    set_catalog_selection_value(project_id, location);
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
        project_id = $(e.relatedTarget).data('module-project'),
        name = $(e.relatedTarget).data('module-name'),
        location = $('#editModuleCatalogs');

    $(e.currentTarget).find('input[name="editModuleId"]').val(id);
    $(e.currentTarget).find('input[name="editModuleName"]').val(name);
    $('#editModuleProject').val(project_id);

    set_catalog_selection_value(project_id, location);

    $.getJSON("{% url 'projects:fetch_project_catalogs_members' %}?id={0}&level=module".format(id)).done(function(data){
        $('#editModuleCatalogs').val(data['catalogs']);
    })
});

$('#editModuleProject').on('change', function(){
    var project_id = $(this).val(),
        location = $('#editModuleCatalogs');

    set_catalog_selection_value(project_id, location);

    $.getJSON("{% url 'projects:fetch_project_catalogs_members' %}?id={0}&level=module".format(module_id)).done(function(data){
        $('#editModuleCatalogs').val(data['catalogs']);
    })
});

$('.editModule form').on('submit', function(){
    var name = $('#editModuleName').val();

    if (name == ''){
        showErrMsg('#editModuleErrMessage', 'Name is Empty');
        return false;
    }
});

function set_catalog_selection_value(project_id, location){
    $.getJSON("{% url 'projects:fetch_project_catalogs_members' %}?id={0}&level=project".format(project_id)).done(function(data){
        var option = '';
        $.each(data['catalogs_module'], function(index, value){
            option += '<option value={0}>{1}</option>'.format(value['id'], value['name']);
        });

        location.empty().append(option);

    })
}
