function sse() {
    var source = new EventSource('/stream');
    var alert_division = document.getElementById('log');
    source.onmessage = function(e) {
        event = JSON.parse(e.data);
        id = event.receiver_id + event.beacon_id;
        alert_division.append(event + "<hr />")
    };



sse();