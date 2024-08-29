async function stream_audio(){
	const ws = new WebSocket("ws://localhost:8000/stream/audio");
	ws.onopen = async () => {
		console.log("WebSocket connection established");
	};

	ws.onmessage = (event) => {
		const transcriptionDiv = document.getElementById('chat_log');
	    transcriptionDiv.innerHTML += event.data;
	};

	ws.onclose = () => {
		console.log('WebSocket connection closed');
	};

	ws.onerror = (event) => {
		console.log('WebSocket error:', event);
	};
	let mediaRecorder;
    navigator.mediaDevices.getUserMedia({ audio: true })
	.then(stream => {
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = event => {
            if (event.data.size > 0) {
                ws.send(event.data);
            }
        };
        mediaRecorder.start(100);
    })
    .catch(error => console.error("Error accessing microphone: ", error));
};