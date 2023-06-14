
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var info_received = [];
 
    var queries = [];
    var completion = [];

    //receive data from server
    socket.on('SatoriResults', function(msg) {
    console.log("Received Results?????  "); 
    console.log("Received Results " + msg.SearchResults); 

    info_received.push('</br>' + msg.SearchResults)
    info_string = '';
    for (var i = 0; i < info_received.length; i++){
        info_string = info_string + '<p>' + info_received[i] + '</p>';
    }
        $('#datastore_name').html(info_string);
    });

    //receive data from server
    socket.on('QueryInfo', function(msg) {
    console.log("Received Queries " + msg.Queries);  

    queries.push(msg.Queries)
    query_string = '';
    for (var i = 0; i < queries.length; i++){
        query_string = query_string + '<p>' + queries[i] + '</p>';
    }
        $('#queries').html(query_string);
    });

    //receive data from server
    socket.on('Completion', function(msg) {
    console.log("Received Completion " + msg.Complete);  

    completion.push(msg.Complete)
    completion_string = '';
    for (var i = 0; i < completion.length; i++){
        completion_string = completion_string + '<p>' + completion[i] + '</p>';
    }
        $('#completion').html(completion_string);
    });



});
