const roomId = JSON.parse(document.getElementById('chat-id').textContent);

const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${roomId}/`);

chatSocket.onmessage = (e) => {
    const data = JSON.parse(e.data);
    document.querySelector('#chatLog').innerHTML += `<div>${data.message}</div>`;
};

