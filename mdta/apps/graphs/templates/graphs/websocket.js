var connected_msg = 'MDTA WebSocket connected.';

function get_ws_uri(){
    var current_url = '',
        room_id = '',
        room_name = '',
        ws_uri = '';

    current_url = window.location.href.split('/');
    room_id = current_url[current_url.length - 2];
    if (current_url[current_url.length - 3].indexOf('module') >= 0){
        room_name = 'module';
    } else {
        room_name = 'project';
    }
    ws_uri = (window.location.protocol === 'https:') ? "wss://" : "ws://" + window.location.host + '/mdta/{0}_{1}/'.format(room_name, room_id);

    return ws_uri;
}

var ws_uri = get_ws_uri();

var ws4redis = WS4Redis({
    uri: ws_uri,
    connecting: on_connecting,
    connected: on_connected,
    receive_message: receiveMessage,
    disconnected: on_disconnected,
    // heartbeat_msg: '{{ WS4REDIS_HEARTBEAT }}'clear
});


// attach this function to an event handler on your site
function sendMessage(msg) {
    ws4redis.send_message(msg);
}

function on_connecting() {
    // console.log('Websocket is connecting...');
}

function on_connected() {
    // ws4redis.send_message(connected_msg);
}

function on_disconnected(evt) {
    console.log('Websocket was disconnected: ' + JSON.stringify(evt));
}

// receive a message though the websocket from the server
function receiveMessage(msg) {
    msg = JSON.parse(msg);
    if (msg['text'] == connected_msg){
        console.log(msg['text'])
    } else {
        reDrawGraph(msg['text']);
    }
}

function reDrawGraph(node) {
    var cy_nodes = cy_nodes_default,
        cy_edges = cy_edges_default,
        view_option = $('#text').text().trim();

    // console.log(view_option)
    if (view_option === 'Data Gaps') {
        if (typeof cy_nodes_gap !== 'undefined') {
            // console.log('Project', cy_nodes_gap)
            cy_nodes = cy_nodes_gap
        } else if (typeof cy_edges_gap !== 'undefined') {
            // console.log('Module', cy_edges_gap)
            cy_edges = cy_edges_gap
        }
    }

    // var cy_nodes = cy_nodes_default;
    node = JSON.parse(node);

    $.each(cy_nodes, function () {
        if (this.data.id === node.node_id){
            this.renderedPosition = node.position;
            return false
        }
    });

    cy.elements().remove();
    cy = create_cy_object(cy_nodes, cy_edges);
}
