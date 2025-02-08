const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

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

  // アプリ起動時に最初のページを表示
  mainWindow.loadFile(path.join(__dirname, 'index.html'));

  // ページ遷移イベントのリスナー
  ipcMain.on('navigate', (event, page) => {
    console.log(`Navigating to: ${page}`); // デバッグ用
    mainWindow.loadFile(path.join(__dirname, page)).catch(err => console.error('Failed to load file:', err));
  });
});
