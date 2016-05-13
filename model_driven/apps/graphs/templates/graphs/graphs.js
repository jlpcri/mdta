/**
 * Created by sliu on 5/12/16.
 */
// String format custom method
String.prototype.format = function () {
    var s = this,
        i = arguments.length;

    while (i--) {
        s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
    }
    return s;
};

$(document).ready(function(){
    $('#subnav-tabs').find('a[href="#projects"]').tab('show');
});

$('.editNodeType').on('show.bs.modal', function(e){
    var node_type_id = $(e.relatedTarget).data('node-type-id'),
        node_type_name = $(e.relatedTarget).data('node-type-name'),
        node_type_keys = $(e.relatedTarget).data('node-type-keys');

    $(e.currentTarget).find('input[name="editNodeTypeId"]').val(node_type_id);
    $(e.currentTarget).find('input[name="editNodeTypeName"]').val(node_type_name);
    $(e.currentTarget).find('input[name="editNodeTypeKeys"]').val(node_type_keys);

    $('.editNodeType .modal-title').html('Node Type Edit - ' + node_type_name)
});