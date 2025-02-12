let socket;

async function startChat() {
    const username = document.getElementById("username").value;
    const role = document.getElementById("role").value;

    let chat_id;

    if (role === 'user') {
        const response = await fetch(`/create_chat/${username}/user`);
        const data = await response.json();
        chat_id = data.chat_id;

        window.history.pushState({}, "", `/chat/${chat_id}/${username}`);
        socket = new WebSocket(`ws://${window.location.host}/ws/${chat_id}/${username}/user`);
    } else {
        const response = await fetch(`/assign_supporter/${username}`);
        const data = await response.json();
        chat_id = data.chat_id;

        window.history.pushState({}, "", `/chat/${chat_id}/${username}`);
        socket = new WebSocket(`ws://${window.location.host}/ws/${chat_id}/${username}/supporter`);
    }

    socket.onopen = () => {
        document.getElementById("login").style.display = "none";
        document.getElementById("chat").style.display = "block";
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const chatBox = document.getElementById("chat-box");
        const messageDiv = document.createElement("div");

        if (data.system) {
            messageDiv.innerText = data.system;
            messageDiv.style.fontStyle = "italic";
        } else {
            messageDiv.innerText = `${data.sender}: ${data.message}`;
            messageDiv.classList.add(data.sender === username ? "user" : "supporter");
        }

        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    socket.onclose = () => {
        alert("Connection closed.");
        location.reload();
    };
}


function sendMessage() {
    const message = document.getElementById("message").value;
    if (message) {
        socket.send(message);
        document.getElementById("message").value = "";
    }
}
