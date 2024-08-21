const ws = new WebSocket("ws://localhost:8000/stream/audio");

async function stream_audio(){

    ws.onopen = async () => {
	    console.log("WebSocket connection established");

	    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
	    const mediaRecorder = new MediaRecorder(stream);

	    mediaRecorder.ondataavailable = event => {
	        if (event.data.size > 0) {
	            ws.send(event.data);
	        }
	    };

	    mediaRecorder.start(25); // Send audio data every 25 milliseconds
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
};
