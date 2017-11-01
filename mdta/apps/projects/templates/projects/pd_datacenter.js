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