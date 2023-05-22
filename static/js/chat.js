const user_id = getCookie('user_id');
const user_token = getCookie('token');
const chat_id = document.querySelector('[data-sf-chat]').dataset.sfChat;

const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const chatSocket = new WebSocket(`${protocol}//${window.location.host}/ws/chat/${chat_id}/?token=${user_token}`);

const messageInputDom = document.querySelector('#chat-message-input');
const submitButton = document.querySelector('#chat-message-submit');
const chatLogDom = document.querySelector('#chatLog');

const dateFormatter = new Intl.DateTimeFormat('uk-UA', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
    hour12: false,
});

const scrollLogDown = () => chatLog.scrollTo(0, chatLog.scrollHeight);

const renderMessage = (data) => {
    const author = data.author;
    const isCurrentUser = author.id == user_id;
    const authorName = isCurrentUser ? 'Ви' : `<a href="/profile/detail/${author.id}">@${author.username}</a>`;
    const formattedDate = dateFormatter.format(new Date(data.date_created));

    return `
      <div href="#" class="list-group-item list-group-item-action">
        <div class="d-flex w-100 justify-content-between">
          <h6 class="mb-1">${authorName}</h6>
          <small>${formattedDate}</small>
        </div>
        <h5 class="mb-1">${data.body}</h5>
      </div>
    `;
}

const handleMessage = (e) => {
    const data = JSON.parse(e.data);
    console.log(data);
    chatLogDom.innerHTML += renderMessage(data);
    scrollLogDown();
}

const handleClose = (e) => {
    console.log('🙀🙀 Chat socket closed unexpectedly');
}

const handleKeyUp = (e) => e.keyCode === 13 && submitButton.click();

const handleSubmit = (e) => {
    const body = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'chat_group': chat_id,
        'body': body
    }));
    messageInputDom.value = '';
}

chatSocket.addEventListener('message', handleMessage);
chatSocket.addEventListener('close', handleClose);

messageInputDom.focus();
messageInputDom.onkeyup = handleKeyUp;
submitButton.onclick = handleSubmit;

window.addEventListener('DOMContentLoaded', scrollLogDown);