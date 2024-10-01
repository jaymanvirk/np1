async function stream_audio(){
	const ws = new WebSocket("ws://localhost:8000/stream/v1/audio");
	ws.binaryType = "arraybuffer";
	const transcriptionDiv = document.getElementById('chat_log');
	const audioElement = document.getElementById('audio');

	const audioContext = new (window.AudioContext || window.webkitAudioContext)();

	ws.onopen = async () => {
		console.log("WebSocket connection established");
	};

	ws.onmessage = async (event) => {
		try {
		    const data = event.data;
	    	//transcriptionDiv.innerHTML += data + "<br>";
	    	const buffer = await audioContext.decodeAudioData(data);
	        const source = audioContext.createBufferSource();
	        source.buffer = buffer;
	        source.connect(audioContext.destination);
	        source.start(0);
        } catch (error) {
            console.error("Error decoding audio data", error);
        };
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
        mediaRecorder.start(500);
    })
    .catch(error => console.error("Error accessing microphone: ", error));
};

