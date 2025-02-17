const { ipcRenderer } = require('electron');

document.addEventListener('DOMContentLoaded', () => {

    const nextButton = document.getElementById('next-button');
    const createRoomButton = document.getElementById('create-room-button');
    const joinRoomButton = document.getElementById('join-room-button');

    if (nextButton) {
        nextButton.addEventListener('click', () => {
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
            const { PythonShell } = require('python-shell');
            const path = require('path');
            
            let options = {
                scriptPath: path.join(__dirname, ''),
                pythonPath: 'python3',
                args: [JSON.stringify({ operation: 1, room_name: "test", password: "1234" })]
            };
            
            console.log("🚀 Python を実行します: ", options);
            
            let shell = new PythonShell('script.py', options);
            ipcRenderer.send('navigate', 'chat-room.html');
        });
    }

    if (joinRoomButton) {
        joinRoomButton.addEventListener('click', () => {
            ipcRenderer.send('navigate', 'chat-room.html');
        });
    }
});
