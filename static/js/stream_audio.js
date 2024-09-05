async function stream_audio(){
	const ws = new WebSocket("ws://localhost:8000/stream/audio");
	const transcriptionDiv = document.getElementById('chat_log');
	const audioElement = document.getElementById('audio');

	ws.onopen = async () => {
		console.log("WebSocket connection established");
	};

	ws.onmessage = (event) => {
	    transcriptionDiv.innerHTML += event.data + "<br>";
	};

	ws.onclose = () => {
		console.log('WebSocket connection closed');
	};

	ws.onerror = (event) => {
		console.log('WebSocket error:', event);
	};

	// let mediaRecorder;
	// const numChannels = 1; // Mono audio

	// navigator.mediaDevices.getUserMedia({ audio: true })
	//     .then(stream => {
	//         mediaRecorder = new MediaRecorder(stream);
	//         const audioTrack = stream.getAudioTracks()[0];
	//         const settings = audioTrack.getSettings();
	// 		const sampleRate = settings.sampleRate;

	//         mediaRecorder.ondataavailable = event => {
	//             if (event.data.size > 0) {
	//                 const audioBlob = event.data;
	//                 const arrayBufferPromise = audioBlob.arrayBuffer();

	//                 arrayBufferPromise.then(arrayBuffer => {
	//                     const audioData = new Uint8Array(arrayBuffer);
	//                     const header = createWavHeader(sampleRate, numChannels, audioData.length);
	//                     const headerView = new Uint8Array(header);

	//                     // Create a new Uint8Array to hold the header and audio data
	//                     const combinedData = new Uint8Array(headerView.length + audioData.length);
	//                     combinedData.set(headerView, 0);
	//                     combinedData.set(audioData, headerView.length);
	//                     // Convert the combined data to a Blob
    //         			const audioBlobWithHeader = new Blob([combinedData], { type: 'audio/wav' });
	//                     ws.send(audioBlobWithHeader);
	//                 });
	//             }
	//         };
	//         mediaRecorder.start(250);
	//     })
	//     .catch(error => console.error("Error accessing microphone: ", error));
	let mediaRecorder;
    navigator.mediaDevices.getUserMedia({ audio: true })
	.then(stream => {
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = event => {
            if (event.data.size > 0) {
	            ws.send(event.data);
	            console.log(event.data);
            }
        };
        mediaRecorder.start(100);
    })
    .catch(error => console.error("Error accessing microphone: ", error));

	// navigator.mediaDevices.getUserMedia({
	//     audio: {
	//         sampleRate: 16000,
	//         channelCount: 1
	//     }
	// })
    // .then(stream => {
	//     let audioContext = new (window.AudioContext || window.webkitAudioContext)();
	// 	const source = audioContext.createMediaStreamSource(stream);
	// 	let scriptProcessor = audioContext.createScriptProcessor(1024, 1, 1);

	// 	source.connect(scriptProcessor);
	// 	scriptProcessor.connect(audioContext.destination);

	// 	scriptProcessor.onaudioprocess = (event) => {
	//         const audioData = event.inputBuffer.getChannelData(0);
	//         ws.send(audioData);
	// 	};
	// })
   	// .catch(error => {
    //     console.error('Error accessing audio stream:', error);
    // });
};


function createWavHeader(sampleRate, numChannels, dataLength) {
    const buffer = new ArrayBuffer(44);
    const view = new DataView(buffer);

    // RIFF identifier
    view.setUint32(0, 0x52494646, false); // 'RIFF'
    // file length
    view.setUint32(4, 36 + dataLength, true);
    // RIFF type
    view.setUint32(8, 0x57415645, false); // 'WAVE'
    // format chunk identifier
    view.setUint32(12, 0x666d7420, false); // 'fmt '
    // format chunk length
    view.setUint32(16, 16, true);
    // sample format (raw)
    view.setUint16(20, 1, true);
    // channel count
    view.setUint16(22, numChannels, true);
    // sample rate
    view.setUint32(24, sampleRate, true);
    // byte rate (sampleRate * blockAlign)
    view.setUint32(28, sampleRate * numChannels * 2, true);
    // block align (channelCount * bytesPerSample)
    view.setUint16(32, numChannels * 2, true);
    // bits per sample
    view.setUint16(34, 16, true);
    // data chunk identifier
    view.setUint32(36, 0x64617461, false); // 'data'
    // data chunk length
    view.setUint32(40, dataLength, true);

    return buffer;
}