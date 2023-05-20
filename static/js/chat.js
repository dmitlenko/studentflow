const user_id = getCookie('user_id');
const user_token = getCookie('token');
const chat_id = document.querySelector('[data-sf-chat]').dataset.sfChat;

const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const chatSocket = new WebSocket(`${protocol}//${window.location.host}/ws/chat/${chat_id}/`);
const chatLog = document.querySelector('#chatLog');

function scrollLogDown() {
    chatLog.scrollTo(0, chatLog.scrollHeight);
}

function renderMessage(userId, username, message, date_created) {
    let output =
        `<div href="#" class="list-group-item list-group-item-action" aria-current="true">
            <div class="d-flex w-100 justify-content-between">` + (
            userId == user_id ? `<h6 class="mb-1">Ви</a></h6>` :
                `<h6 class="mb-1"><a href="/profile/detail/${userId}">@${username}</a></h6>`
        ) + `<small>${date_created}</small>
            </div>
            <h5 class="mb-1">${message}</p>
        </div>`;
    chatLog.innerHTML += output;
}

chatSocket.addEventListener('message', function (e) {
    const data = JSON.parse(e.data);
    renderMessage(data.userId, data.username, data.message, data.date_created);
    scrollLogDown();
});

chatSocket.addEventListener('close', function (e) {
    // TODO: add closed connection modal
    console.log('🙀🙀 Chat socket closed unexpectedly');
});

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = (e) => {
    if (e.keyCode === 13) {
        document.querySelector('#chat-message-submit').click();
    }
}

document.querySelector('#chat-message-submit').onclick = (e) => {
    const messageInputDom = document.querySelector('#chat-message-input');
    const body = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'author': user_token,
        'chat_group': chat_id,
        'body': body
    }));
    messageInputDom.value = '';
}

window.addEventListener("DOMContentLoaded", function (e) {
    scrollLogDown();
})