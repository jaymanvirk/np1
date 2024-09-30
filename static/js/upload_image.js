async function upload_image(file){
    const ws = new WebSocket("ws://localhost:8000/stream/v1/image");

    ws.onopen = () => {
        const reader = new FileReader();
        reader.onloadend = (event) => {
            const image_data = new Uint8Array(event.target.result);
            const chunk_size = 1024;
            ws.send(image_data.length/chunk_size);
            for (let i = 0; i < image_data.length; i += chunk_size) {
                ws.send(image_data.slice(i, i + chunk_size));
            };
        };
        reader.readAsArrayBuffer(file);
    };

    ws.onmessage = (event) => {
      console.log(event.data);
    };

    ws.onclose = () => {
      console.log('WebSocket connection closed');
    };

    ws.onerror = (event) => {
      console.log('WebSocket error:', event);
    };
}

function select_image(event) {
    const file = event.target.files[0];
    preview_image(file);
    upload_image(file);
}

function drag_image(event) {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'copy';
}

function drop_image(event) {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    upload_image(file);
}

function preview_image(file) {
    preview_image = document.getElementById('preview_image');
    const reader = new FileReader();
    reader.onload = function(event) {
        preview_image.src = event.target.result;
    };
    reader.readAsDataURL(file);
};
