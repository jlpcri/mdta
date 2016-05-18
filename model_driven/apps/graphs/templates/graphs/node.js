/**
 * Created by sliu on 5/18/16.
 */
$('#id_type').on('change', function(){
    var item_id = $(this).find('option:selected').val();
    load_keys_from_type_contents(item_id);
});

$(document).ready(function(){
    var item_id = $('#id_type').find('option:selected').val();
    load_keys_from_type_contents(item_id);
});

function load_keys_from_type_contents(item_id){
    $.getJSON("{% url 'graphs:get_keys_from_type' %}?id={0}&type=node".format(item_id)).done(function(data){
        var contents = '';
        $.each(data, function(k, v){
            contents += '<div class=\'col-xs-2\'><label>{0}: </label> <input name=\'{0}\'/></div>'.format(data[k]);
        });
        //console.log(contents)
        $('#project-node-new-data-input').html(contents)
    })
}