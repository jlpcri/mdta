/**
 * Created by sliu on 5/18/16.
 */

// Calculate cytoscape graph height
var graph_height = calculate_graph_height();
function calculate_graph_height() {
    var graph_height = 0,
        screen_avail_height = window.screen.availHeight;
    switch (true) {
        case (screen_avail_height >= 999):
            graph_height = 850;
            break;
        case (screen_avail_height >= 900):
            graph_height = 800;
            break;
        case (screen_avail_height > 850):
            graph_height = 750;
            break;
        default:
            graph_height = 500;
    }
    return graph_height;
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



