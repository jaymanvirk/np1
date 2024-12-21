async function stream_audio(){
    const ws = new WebSocket("wss://kompjuut.com/stream/v1/audio");
    ws.binaryType = "arraybuffer";

    const audio_context = new (window.AudioContext || window.webkitAudioContext)();
    let audio_queue = [];
    let is_playing = false;
    function play_next_queue() {
        if (audio_queue.length === 0) {
            is_playing = false;
            return;
        }

        is_playing = true;
        const buffer = audio_queue.shift();
        const source = audio_context.createBufferSource();
        source.buffer = buffer;
        source.connect(audio_context.destination);

        source.onended = play_next_queue;
        source.start(0);
    }
    ws.onopen = async () => {
        console.log("WebSocket connection established");
    };

    ws.onmessage = async (event) => {
        try {
            const data = event.data;
            if (typeof data === 'string'){
                process_message(data);
                scroll_to_bottom();
            } else {
                const buffer = await audio_context.decodeAudioData(data);
                audio_queue.push(buffer);
                if (!is_playing) {
                    play_next_queue();
                }
 
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
        console.log('WebSocket error:', event);
        mediaRecorder.stop();
    };

    let mediaRecorder;
    navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = event => {
            if (event.data.size > 0 && ws.readyState === WebSocket.OPEN){
                ws.send(event.data);
            }
        };

        mediaRecorder.start(500);
    })
    .catch(error => console.error("Error accessing microphone: ", error));
};

