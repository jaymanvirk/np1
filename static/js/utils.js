function scroll_to_bottom() {
    window.scrollTo(0, document.body.scrollHeight);
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

function process_message(json_data) {
    const data = JSON.parse(json_data);
    const chat = document.getElementById('chat');
    const m_div = document.querySelector(`div.message[id='${data.meta.id}']`);
    
    if (!m_div) {
        chat.insertAdjacentHTML('beforeend', get_html_message(data));
    }
    
    const m_content = document.querySelector(`div.message[id='${data.meta.id}'] > .media-content`);
    m_content.textContent = data.media.text;
}

