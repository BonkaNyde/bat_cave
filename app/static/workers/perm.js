importScripts('/static/libs/socketio/socket.io.min.js');
const socket_connection = io(self.name);

const connectedPorts = [];



onconnect = function({ports}){
    let port = ports[0];
    connectedPorts.push(port);
    
    // initialize socketio connection

    // Send initial package on open.
    // send_message('socket name ', location)
    connectedPorts.forEach(port => port.postMessage(
        {'perm_worker': 'connected ports '.concat(connectedPorts.length)}
    ));
    
    // what to do when socketio connects
    socket_connection.on('connect', function(){
        // send initial connection request. This gives socketio the client to register
        connectedPorts.forEach(port => port.postMessage(
            {'connected socketio': connectedPorts.length}
        ))
        socket_connection.emit('get_perm');
    });
    socket_connection.on('recv_perm', function(perm){
        connectedPorts.forEach(port => port.postMessage(perm))
    });
};
