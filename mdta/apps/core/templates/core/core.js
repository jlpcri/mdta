/**
 * Created by sliu on 5/18/16.
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

function showErrMsg(location, msg){
    $(location).css({
        'font-size': 15,
        'color': 'blue'
    });
    $(location).html('Error: ' + msg);
}

function load_keys_from_node_edge_type(item_id, location, type){
    $.getJSON("{% url 'graphs:get_keys_from_type' %}?id={0}&type={1}".format(item_id, type)).done(function(data){
        var contents = '';
        $.each(data, function(k, v){
            contents += '<div class=\'row\' style=\'margin-top: 5px;\'>';
			contents += '<div class=\'col-xs-4\'><label>{0}: </label></div>'.format(data[k]);
			contents += '<div class=\'col-xs-8\'><input name=\'{0}\'/></div>'.format(data[k]);
			contents += '</div>';
        });
        //console.log(contents)
        $(location).html(contents)
    })
}

function load_keys_from_node_edge_type_together(item_id, location, type){
    $.getJSON("{% url 'graphs:get_keys_from_type' %}?id={0}&type={1}".format(item_id, type)).done(function(data){
        var contents = '';
        $.each(data, function(k, v){
            contents += '<div class=\'row\' style=\'margin-top: 5px;\'>';
			contents += '<div class=\'col-xs-4\'><label>{0}: </label></div>'.format(data[k]);
			contents += '<div class=\'col-xs-8\'><input name=\'{0}\'/></div>'.format(type + '_' + data[k]);
			contents += '</div>';
        });
        //console.log(contents)
        $(location).html(contents)
    })
}