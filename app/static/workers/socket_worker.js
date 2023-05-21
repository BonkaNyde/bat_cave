"use strict"
// socketio js library

// importScripts('/static/libs/socketio/socket.io.min.js');
// // socketio initializatioin
// const socket_connection = io(self.name, {
//     transports: ["websocket", "polling"]
// });


const connectedPorts = [];

const postToClient = function(event, data=null){
    `Send message to main thread.
    `
    let payload = JSON.stringify({
        "event": event,
        "data": data
    });
    connectedPorts.forEach(port => port.postMessage(payload));
};


function handleFormSubmit(post_url, form_data){
    let x = new fetch(post_url, {
        method: 'post',
        body: form_data
    })
    return x;
};


onconnect = function({ports}){
    let port = ports[0];
    connectedPorts.push(port);
    

    postToClient('worker connected', 'connected ports '.concat(connectedPorts.length));

    port.onmessage = (message) => {
        let parsed_message = JSON.parse(message.data);
        action = parsed_message.action;
        sio_event = parsed_message.event;
        data = parsed_message.data;
        // send_message('received message', {"action": 'action'});
        if (action === 'send' && data){
            // Send message to socket;
            // socket_connection.emit(sio_event, data)
            postToClient('event : '.concat(sio_event), data);
        } else if(action === 'unload'){
            // Remove port from connected ports list;
            const index = connectedPorts.indexOf(port);
            connectedPorts.splice(index, 1);
            postToClient('worker unloading port', {"port at index": index});
        } else if (action === ''){

        };
    };
};


onerror = function(e){
    send_message('message worker error', {'error': e});
};
