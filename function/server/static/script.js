let socket;
let username;
let role;

function startChat() {
    username = document.getElementById("username").value;
    role = document.getElementById("role").value;

    if (!username) {
        alert("Please enter username!");
        return;
    }

    socket = new WebSocket(`ws://${window.location.host}/ws/${username}/${role}`);

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
