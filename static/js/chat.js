const roomId = JSON.parse(document.getElementById('chat-id').textContent);

const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${roomId}/`);

chatSocket.onmessage = (e) => {
    const data = JSON.parse(e.data);
    document.querySelector('#chatLog').innerHTML += `<div>${data.message}</div>`;
}

chatSocket.onclose = (e) => {
    console.log('🙀🙀 Chat socket closed unexpectedly');
}

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = (e) => {
    if (e.keyCode === 13) {  
        document.querySelector('#chat-message-submit').click();
    }
}

document.querySelector('#chat-message-submit').onclick = (e) => {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
}