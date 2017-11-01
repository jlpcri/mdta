// String format custom method
String.prototype.format = function () {
    var s = this,
        i = arguments.length;

    while (i--) {
        s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
    }
    return s;
};

var last_db_id = '{{ last_db_id }}',
    initial_db_id = '{{ project_dbset.0.id }}';
if (last_db_id !== '') {
    $('a[href="#dbset-db-{0}"]'.format(last_db_id)).click()
} else if(initial_db_id !== ''){
    $('a[href="#dbset-db-{0}"]'.format(initial_db_id)).click()
}

$('.newDbsetDb form').on('submit', function (e) {
    var name = $(e.currentTarget).find('input[name="name"]').val();

    if (name === ''){
        showErrMsg('#dbSetDbNewErrMessage', 'Name is empty');
        return false;
    }
});

$('.editDbsetDb').on('show.bs.modal', function (e) {
    var dbset_db_id = $(e.relatedTarget).data('dbset-db-id'),
        dbset_db_name = $(e.relatedTarget).data('dbset-db-name');

    $(e.currentTarget).find('input[name="datasetDbEditId"]').val(dbset_db_id);
    $(e.currentTarget).find('input[name="datasetDbEditName"]').val(dbset_db_name);

});

$('.editDbsetDb form').on('submit', function (e) {
    var name = $(e.currentTarget).find('input[name="datasetDbEditName"]').val();

    if (name === ''){
        showErrMsg('#dbSetDbEditErrMessage', 'Name is empty');
        return false;
    }
});