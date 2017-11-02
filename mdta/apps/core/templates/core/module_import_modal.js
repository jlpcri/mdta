//Three steps for project imports modules from prompt lists excel
var project_id = '{{project.id}}',
    projects_options = $('#module-import-modal-2 select option').clone(),
    project_option = projects_options.filter(function (t) {
        return parseInt(this.value) === parseInt(project_id);
    });

$('#module-import-modal-1').on('show.bs.modal', function () {
    $("#mySideBar").toggleClass("sidebar-nav-toggled");
    $(".backdrop").toggle();
});

$('.importToStep2').click(function () {
    $('#module-import-modal-2 select').html(project_option);
    $('#module-import-modal-2').modal('show')
});

$('#import_to_step_3').click(function () {
    $('#module-import-modal-3').modal('show')
});

//File upload form
$('.moduleImport input:file').on('change', function () {
    var input = $(this),
        numFiles = input.get(0).files ? input.get(0).files.length : 1,
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselect', [numFiles, label]);
});

$('.moduleImport input:file').on('fileselect', function (event, numFiles, label) {
    var input = $(this).parents('.input-group').find(':text'),
        log = numFiles > 1 ? numFiles + ' files selected' : label;

    if (input.length) {
        input.val(log);
    } else {
        if (log) alert(log);
    }
});

$('#language_add').click(function () {
    var name = $('#module-import-modal-2 #id_name').val(),
        root_path = $('#module-import-modal-2 #id_root_path').val(),
        lan_list = [];

    $('#module-import-modal-2 .projectLanguages li').each(function () {
        lan_list.push($(this).text())
    });

    if (name === ''){
        showErrMsg('#newLanguageErrMessage', 'Language is Empty');
        return false;
    } else if (lan_list.indexOf(name) >= 0){
        showErrMsg('#newLanguageErrMessage', 'Language is Duplicated');
        return false;
    } else if (!isURL(root_path)) {
        showErrMsg('#newLanguageErrMessage', 'Root Path is not valid');
        return false
    }else{
        var lan = {
            'project_id': $('#module-import-modal-2 #id_project').val(),
            'name': name,
            'root_path': $('#module-import-modal-2 #id_root_path').val()
        },
        data = {
            'lan': JSON.stringify(lan),
            'csrfmiddlewaretoken': '{{csrf_token}}'
        };
        $.ajax({
            type: 'POST',
            data: data,
            url: '{% url "projects:language_new_from_module_import" %}',
            dataType: 'json'
        }).done(function (data) {
            var html = '';
            $.each(data, function (idx, value) {
                html += '<li>{0}</li>'.format(value['lan_name']);
            });
            $('.projectLanguages').html(html);
            $('#module-import-modal-2 #id_name').val('');
            $('#newLanguageErrMessage').html('');
        })
    }
});

function isURL(str) {
    var pattern = new RegExp(
        '^(https?:\\/\\/)?'+ // protocol
        // '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.?)+[a-z]{2,}|'+ // domain name
        // '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
        '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
        '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
        '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
    return pattern.test(str);
}

$('#import-language-edit-modal').on('show.bs.modal', function(e){
    var language_id = $(e.relatedTarget).data('language-id');

    $.getJSON("{% url 'projects:get_language_detail_for_import_module'%}?lan_id={0}".format(language_id)).done(function (data) {
        var name = data['lan_name'],
            root_path = data['root_path'];

        $(e.currentTarget).find('input[name="editLanguageId"]').val(language_id);
        $(e.currentTarget).find('select').html(project_option);
        $(e.currentTarget).find('input[name="editLanguageName"]').val(name);
        $(e.currentTarget).find('input[name="editLanguageRootPath"]').val(root_path);
    });
});