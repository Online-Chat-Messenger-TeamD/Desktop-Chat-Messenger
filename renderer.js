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
            const roomName = document.getElementById('room-name').value.trim();
            const password = document.getElementById('password').value.trim();
            
            if (!roomName || !password) {
                alert('ルーム名とパスワードを入力してください');
                return;
            }

            let options = {
                scriptPath: path.join(__dirname, ''),
                pythonPath: 'python3',
                args: [JSON.stringify({ operation: 1, room_name: roomName, password: password })]
            };
            
            console.log("🚀 Python を実行します: ", options);
            
            // 変数shellにアクセスするために、letで宣言
            let shell = new PythonShell('script.py', options);

            // ルーム作成直後にチャットルームに遷移すると、Broken Pipeエラーが発生するため、ちょっと待つ必要がありそう
            // ipcRenderer.send('navigate', 'chat-room.html');
        });
    }

    if (joinRoomButton) {
        joinRoomButton.addEventListener('click', () => {
            const { PythonShell } = require('python-shell');
            const path = require('path');
            const roomName = document.getElementById('room-name').value.trim();
            const password = document.getElementById('password').value.trim();
            
            if (!roomName || !password) {
                alert('ルーム名とパスワードを入力してください');
                return;
            }

            let options = {
                scriptPath: path.join(__dirname, ''),
                pythonPath: 'python3',
                args: [JSON.stringify({ operation: 2, room_name: roomName, password: password })]
            };
            
            console.log("🚀 Python を実行します: ", options);
            
            let shell = new PythonShell('script.py', options);
            // ルーム作成直後にチャットルームに遷移すると、Broken Pipeエラーが発生するため、ちょっと待つ必要がありそう
            // ipcRenderer.send('navigate', 'chat-room.html');
        });
    }
});
