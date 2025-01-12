async function stream_audio(){
    const ws = new WebSocket("wss://kompjuut.com/stream/v1/audio");
    ws.binaryType = "arraybuffer";

    const audio_manager = new AudioManager()

    let mediaRecorder;
    navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = event => {
            if (event.data.size > 0 && ws.readyState === WebSocket.OPEN){
                ws.send(event.data);
            }
        };

        mediaRecorder.start(221);
    })
    .catch(error => console.error("Error accessing microphone: ", error));

    ws.onopen = async () => {
        console.log("WebSocket connection established");
    };

    ws.onmessage = async (event) => {
        try {
            const data = event.data;
            if (typeof data === 'string'){
                process_data(data, audio_manager);
            } else {
                audio_manager.play_audio(data);
            }
        } catch (error) {
            console.error("Error decoding audio data", error);
        };
    };

    ws.onclose = () => {
        console.log('WebSocket connection closed');
        mediaRecorder.stop();
    };

    ws.onerror = (event) => {
        console.error('WebSocket error:', event);
        mediaRecorder.stop();
    };
};

