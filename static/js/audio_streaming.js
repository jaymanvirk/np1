let mediaRecorder;
let ws;

async function start_streaming(){
	const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start(1);

    ws = new WebSocket('ws://localhost:8000/ws');
    ws.binaryType = 'arraybuffer';
    ws.onopen = () => {
        console.log('WebSocket connection opened');
    };
    ws.onmessage = function(evt) {
    	console.log('RESPONSE: ' + evt.data);
	};
	ws.onerror = function(evt) {
    	console.log('ERROR: ' + evt.data);
	};

    mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
            ws.send(event.data);
        }
    };
}

function stop_streaming(){
    mediaRecorder.stop();
	ws.close();
}