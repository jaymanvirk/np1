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
    const data = JSON.parse(data);
    if (data.type == "command") {
        process_command(data, object);
    else {
        process_message(data)
        scroll_to_bottom();
    }
}


function process_command(data, object) {
    if (data.command == "stop_audio") {
        object.stop_audio();
    }
}


function process_message(json_data) {
    const chat = document.getElementById('chat');
    const m_div = document.querySelector(`div.message[id='${data.meta.id}']`);
    
    if (!m_div) {
        chat.insertAdjacentHTML('beforeend', get_html_message(data));
    }
    
    const m_content = document.querySelector(`div.message[id='${data.meta.id}'] > .media-content`);
    m_content.textContent = data.media.text;
}

