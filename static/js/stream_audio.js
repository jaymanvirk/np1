async function stream_audio(){
	const ws = new WebSocket("ws://localhost:8000/stream/audio");

    let mediaRecorder;
	const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    
    mediaRecorder.ondataavailable = event => {
        ws.send(event.data);
    };

   	ws.onmessage = (event) => {
  		const transcriptionDiv = document.getElementById('chat_log');
        transcriptionDiv.innerHTML += event.data;
    };

   	ws.onopen = () => {
      console.log('WebSocket connection open');
    };

    ws.onclose = () => {
      console.log('WebSocket connection closed');
    };

    ws.onerror = (event) => {
      console.log('WebSocket error:', event);
    };
};
