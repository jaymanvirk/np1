async function upload_image(file){
    const image_array = get_image_array(file)
    preview_image(image_array);
    const ws = new WebSocket("ws://localhost:8000/upload/images");

    ws.onopen = () => {
      const image_data = new Uint8Array(image_array);
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

function preview_image(image_array) {
    preview_image = document.getElementById('preview_image');
    preview_image.src = image_data
    // if (file.type.startsWith('image/')) {
    //     const reader = new FileReader();
    //     reader.onload = function(event) {
    //         preview_image.src = event.target.result;
    //     };
    //     reader.readAsDataURL(file);
    // }
}

function get_image_array(file){
    const reader = new FileReader();
    reader.onloadend = (event) => {
        return event.target.result;
    };

    return reader.readAsArrayBuffer(file);
}
