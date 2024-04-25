// Ensure the script runs after the full document content is loaded
document.addEventListener('DOMContentLoaded', function () {
    // Initialize a connection to the server-side Socket.IO
    let socket = io();

    // Function to send movement commands to the server
    function sendCommand(direction, moving) {
        // Emit a control event with the direction and movement status (true for move, false for stop)
        socket.emit('control', { direction: direction, moving: moving });
    }

    socket.on('obstruction', function (data) {
        const btn = document.getElementById(`${data.direction}-button`);
        if (data.status === 'blocked') {
            btn.disabled = true;
            btn.style.backgroundColor = 'red';  // Change the color to red to indicate obstacle
        } else {
            btn.disabled = false;
            btn.style.backgroundColor = '';  // Reset the background color
        }
    });

    // Add event listeners to all buttons
    document.querySelectorAll('button').forEach(button => {
        // On button press, send a command to start moving in the direction indicated by the button's text
        button.onmousedown = function () {
            sendCommand(this.textContent.trim().toLowerCase(), true);
        };
        // On button release, send a command to stop moving in the direction indicated by the button's text
        button.onmouseup = function () {
            sendCommand(this.textContent.trim().toLowerCase(), false);
        };
    });
});

// Handle connection errors
socket.on('connect_error', (err) => {
    console.error('Connection failed: ', err);
});

// Attempt to reconnect if disconnected
socket.on('disconnect', () => {
    console.log('Disconnected from server. Attempting to reconnect...');
    socket.connect();
});
