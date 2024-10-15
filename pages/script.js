const socket = io()

socket.on('result', async (data) => {
    addMessage(data.text, data.file, "received")
})
// Función para añadir un mensaje al chat
function addMessage(content, file = null, type = 'sent') {
    const messageContainer = document.getElementById('chat-messages');

    // Crear el contenedor del mensaje
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', type);  // Tipo puede ser 'sent' o 'received'

    if (type != 'sent') {
        messageElement.innerHTML = `
    <h3>Respuesta: </h3>    
    <br>
    <p>${content}</p>
    <br><br>

    <a href='#'>${file}</a>

    `;
    } else {
        messageElement.innerHTML = `
    <p>${content}</p>`;
    }

    // Añadir el mensaje al contenedor de mensajes
    messageContainer.appendChild(messageElement);

    // Deslizar automáticamente al fondo cuando se agrega un nuevo mensaje
    const chatWindow = document.getElementById('chat-window');
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Evento para el botón de enviar
document.getElementById('send-btn').addEventListener('click', async function () {
    const inputField = document.getElementById('message-input');
    const message = inputField.value.trim();

    let res = await fetch('http://localhost/api/prompt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    })

    if (message) {
        addMessage(message, 'sent');  // Añadir el mensaje del usuario
        inputField.value = '';  // Limpiar el campo de texto
    }
});

// Permitir el envío al presionar la tecla Enter
document.getElementById('message-input').addEventListener('keydown', function (event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        document.getElementById('send-btn').click();  // Simular el click en el botón de enviar
    }
});
