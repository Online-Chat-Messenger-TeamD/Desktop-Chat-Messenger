const { ipcRenderer } = require('electron');

document.addEventListener('DOMContentLoaded', () => {
    console.log("Renderer script loaded"); // デバッグ用

    const nextButton = document.getElementById('next-button');
    const createRoomButton = document.getElementById('create-room-button');
    const joinRoomButton = document.getElementById('join-room-button');

    if (nextButton) {
        nextButton.addEventListener('click', () => {
            console.log("Next button clicked"); // デバッグ用
            const createRoomOption = document.getElementById('create-room-option').checked;
            const joinRoomOption = document.getElementById('join-room-option').checked;

            if (createRoomOption) {
                ipcRenderer.send('navigate', 'create-room.html');
            } else if (joinRoomOption) {
                ipcRenderer.send('navigate', 'join-room.html');
            }
        });
    }

    if (createRoomButton) {
        createRoomButton.addEventListener('click', () => {
            console.log("Create Room button clicked"); // デバッグ用
            ipcRenderer.send('navigate', 'chat-room.html');
        });
    }

    if (joinRoomButton) {
        joinRoomButton.addEventListener('click', () => {
            console.log("Join Room button clicked"); // デバッグ用
            ipcRenderer.send('navigate', 'chat-room.html');
        });
    }
});
