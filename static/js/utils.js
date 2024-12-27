function scroll_to_bottom() {
    const scroll_position = window.scrollY + window.innerHeight;
    const document_height = document.body.scrollHeight;
    if (scroll_position >= document_height - 50) {
        window.scrollTo(0, document.body.scrollHeight);
    }
}

function get_html_message(data) {
    return `
        <div class="message" id="${data.meta.id}">
            <div class="sender display-ib">
                <span class="name">${data.sender.name}</span>
                <span class="colon">:</span>
            </div>
            <div class="media-content display-ib"></div>
        </div>
    `;
}

function process_data(data, object) {
    const data_json = JSON.parse(data);
    if (data_json.type == "command") {
        process_command(data_json, object);
    } else {
        if (object.is_playing && data_json.sender.name != "K"){
            object.stop_audio();
        }
        process_message(data_json)
        scroll_to_bottom();
    }
}


function process_command(data, object) {
    if (data.command == "stop_audio") {
        object.stop_audio();
    }
}


function process_message(data) {
    const chat = document.getElementById('chat');
    const m_div = document.querySelector(`div.message[id='${data.meta.id}']`);
    
    if (!m_div) {
        chat.insertAdjacentHTML('beforeend', get_html_message(data));
    }
    
    const m_content = document.querySelector(`div.message[id='${data.meta.id}'] > .media-content`);
    m_content.textContent = data.media.text;
}

