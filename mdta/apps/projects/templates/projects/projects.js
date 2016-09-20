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


$('.editProject form').on('submit', function(){
    var name = $('#editProjectName').val();

    if (name == ''){
        showErrMsg('#editProjectErrMessage', 'Name is Empty');
        return false;
    }
});

$('.newModule #id_project').on('change', function(){
    var project_id = $(this).val(),
        location = $('.newModule #id_catalog');

    set_catalog_selection_value(project_id, null, location);
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


$('.editModule #id_project').on('change', function(){
    var project_id = $(this).val(),
        module_id = '{{module.id}}',
        location = $('#id_catalog');

    set_catalog_selection_value(project_id, module_id, location);

    $.getJSON("{% url 'projects:fetch_project_catalogs_members' %}?id={0}&level=module".format(module_id)).done(function(data){
        $('#id_catalog').val(data['catalogs']);
    })
});

$('.editModule form').on('submit', function(){
    var name = $('#id_name').val();

    if (name == ''){
        showErrMsg('#editModuleErrMessage', 'Name is Empty');
        return false;
    }
});

function set_catalog_selection_value(project_id, module_id, location){
    $.getJSON("{% url 'projects:fetch_project_catalogs_members' %}?id={0}&level=project".format(project_id)).done(function(data){
        var option = '';
        $.each(data['catalogs_module'], function(index, value){
            option += '<option value={0}>{1}</option>'.format(value['id'], value['name']);
        });

        location.empty().append(option);
    });

    if (module_id) {
        $.getJSON("{% url 'projects:fetch_project_catalogs_members' %}?id={0}&level=module".format(module_id)).done(function (data) {
            location.val(data['catalogs']);
        })
    }
}

