/**
 * Created by sliu on 6/8/16.
 */

var container = document.getElementById('node_in_module');

// provide the data in the vis format
var data = {
    nodes: nodes,
    edges: edges
};
var options = {
    nodes: {
        shape: 'ellipse',
        //fontSize: 10
    },
    edges: {
        //style: 'arrow',
        color: '#000',
        length: 190,
        arrows: 'to'
    },
    width: '100%',
    height: '800px'
};

// initialize your network!
var network = new vis.Network(container, data, options);