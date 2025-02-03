const { ipcRenderer } = require('electron');

document.getElementById('runPython').addEventListener('click', async () => {
  try {
    const result = await ipcRenderer.invoke('run-python');
    document.getElementById('output').innerText = result.message;
  } catch (error) {
    console.error('Error:', error);
  }
});
