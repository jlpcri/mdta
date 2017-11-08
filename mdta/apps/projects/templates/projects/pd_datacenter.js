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

function deleteRow(row){
    $(row).closest('tr').remove();
}

function dbset_db_add_rec(db_id) {
    var keys = ['Inputs', 'Outputs'],
        location = '#dbset-db-table-{0}'.format(db_id),
        newRow = '',
        rowCounter = parseInt($('{0} tr:last'.format(location)).attr('id')) + 1;

    newRow += '<tr id=\'{0}\'>'.format(rowCounter);
    $.each(keys, function (k, v) {
        newRow += '<td><input name=\'{0}_{1}\' style=\'width: 100%\' placeholder={2}></td>'.format(v, rowCounter, 'JSON');
    });
    newRow += '<td class=\'text-center\'><a href=\'#\' onclick=\'deleteRow(this);\'><i class=\'fa fa-trash-o fa-lg\'></i></a></td>';
    newRow += '</tr>';
    $(location).append(newRow)
}

function dbset_db_save(db_id) {
    console.log(db_id)
}

$('.dbsetSaveData').submit(function (event) {
    var fromArray = $(this).serializeArray(),
        db_id = $(this).attr('id').split('-').pop(),
        chunkArray = [];

    while(fromArray.length){
        chunkArray.push(objectifyForm(fromArray.splice(0, 2)))
    }
    var data = {
        'db_id': db_id,
        'db_data': JSON.stringify(chunkArray),
        'csrfmiddlewaretoken': '{{csrf_token}}'
    };
    $.ajax({
        type: 'POST',
        data: data,
        url: '{% url "projects:project_dbset_data_edit" %}',
        dataType: 'json'
    });

    event.preventDefault();
});

function objectifyForm(formArray) {//serialize data function

  var returnArray = {};
  // for (var i = 0; i < formArray.length; i++){
  //   returnArray[formArray[i]['name']] = formArray[i]['value'];
  // }
  $.each(formArray, function (idx, ele) {
      returnArray[ele['name'].split('_')[0]] = ele['value']
  });
  return returnArray;
}