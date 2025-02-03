const { app, BrowserWindow, ipcMain } = require('electron');
const { spawn } = require('child_process');

let mainWindow;

app.whenReady().then(() => {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  mainWindow.loadFile('index.html');
});

// Python スクリプト実行用の IPC ハンドラー
ipcMain.handle('run-python', async () => {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', ['script.py']);

    pythonProcess.stdout.on('data', (data) => {
      resolve(JSON.parse(data.toString()));
    });

    pythonProcess.stderr.on('data', (data) => {
      reject(data.toString());
    });
  });
});
