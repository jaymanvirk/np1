async function stream_audio(){
	const ws = new WebSocket("ws://localhost:8000/stream/audio");
	const transcriptionDiv = document.getElementById('chat_log');
	const audioContext = new (window.AudioContext || window.webkitAudioContext)();
	let scriptProcessor;

	ws.onopen = async () => {
		console.log("WebSocket connection established");
	};

	ws.onmessage = (event) => {
	    transcriptionDiv.innerHTML += event.data + "<br>";
	    // if (event.data instanceof Blob) {
		//     event.data.arrayBuffer().then(buffer => {
		//         audioContext.decodeAudioData(buffer, function(decodedBuffer) {
		//             var source = audioContext.createBufferSource();
		//             source.buffer = decodedBuffer;
		//             source.connect(audioContext.destination);
		//             source.start();
		//         });
		//     });
		// } else {
        //     console.error("Received data is not a Blob:", event.data);
		// }
	};

	ws.onclose = () => {
		console.log('WebSocket connection closed');
	};

	ws.onerror = (event) => {
		console.log('WebSocket error:', event);
	};

  	const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const source = audioContext.createMediaStreamSource(stream);
    scriptProcessor = audioContext.createScriptProcessor(16384, 1, 1);

    source.connect(scriptProcessor);
    scriptProcessor.connect(audioContext.destination);

    scriptProcessor.onaudioprocess = (audioProcessingEvent) => {
	    if (ws.readyState === WebSocket.OPEN) {
	        const audioData = audioProcessingEvent.inputBuffer.getChannelData(0);
	        ws.send(audioData);
	    }
	};

	// let mediaRecorder;
    // navigator.mediaDevices.getUserMedia({ audio: true })
	// .then(stream => {
    //     mediaRecorder = new MediaRecorder(stream);

    //     mediaRecorder.ondataavailable = event => {
    //         if (event.data.size > 0) {
	//             ws.send(event.data);
    //         }
    //     };
    //     mediaRecorder.start(100);
    // })
    // .catch(error => console.error("Error accessing microphone: ", error));
};