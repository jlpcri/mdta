/**
 * Created by sliu on 5/18/16.
 */
// Calculate cytoscape graph height
var graph_height = 0,
    screen_avail_height = window.screen.availHeight;
if (screen_avail_height >= 999) {
    graph_height = 800
} else if (screen_avail_height >= 900){
    graph_height = 680
} else if (screen_avail_height > 850){
    graph_height = 650
} else {
    graph_height = 500
}

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


