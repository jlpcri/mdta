var current_module_id = get_current_module_id(),
    connected_msg = 'MDTA WebSocket connected.';
var ws_uri = (window.location.protocol === 'https:') ? "wss://" : "ws://" + window.location.host + '/mdta/module_{0}/'.format(current_module_id);


var ws4redis = WS4Redis({
    // uri: '{{ WEBSOCKET_URI }}foobar?subscribe-broadcast&publish-broadcast&echo',
    // uri:'{0}module?subscribe-{1}&publish-{1}&echo'.format(ws_uri, 'broadcast'),
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
    console.log('Websocket is connecting...');
}

function on_connected() {
    ws4redis.send_message(connected_msg);
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
    var cy_nodes = cy_nodes_default;
    node = JSON.parse(node);

    $.each(cy_nodes, function () {
        if (this.data.id === node.node_id){
            this.renderedPosition = node.position;
            return false
        }
    });

    cy.elements().remove();
    cy = create_cy_object(cy_nodes, cy_edges_default);
}