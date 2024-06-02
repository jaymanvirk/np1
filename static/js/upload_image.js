async function upload_image(file){
    preview_image(file);
    const ws = new WebSocket("ws://localhost:8000/upload/images");

    ws.onopen = () => {
      const image_data = new Uint8Array(file);
      const chunk_size = 1024;
      for (let i = 0; i < image_data.length; i += chunkSize) {
        ws.send(image_data.slice(i, i + chunkSize));
      }
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
    upload_image(file)
}

function drag_image(event) {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'copy';
}

function drop_image(event) {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    upload_image(file)
}

function previewImage(file) {
    preview_image = document.getElementById('preview_image');
    if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(event) {
            preview_image.src = event.target.result;
        };
        reader.readAsDataURL(file);
    }
}
