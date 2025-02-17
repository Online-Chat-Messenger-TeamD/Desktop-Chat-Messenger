const { PythonShell } = require('python-shell');
const path = require('path');

let options = {
    scriptPath: path.join(__dirname, ''),
    pythonPath: 'python3',
    args: [JSON.stringify({ operation: 1, room_name: "test", password: "1234" })]
};

console.log("🚀 Python を実行します: ", options);

// ✅ `PythonShell.run()` を修正して標準エラーもキャッチ
let shell = new PythonShell('script.py', options);

shell.on('message', (message) => {
    console.log("📩 Python からのメッセージ:", message);
});

shell.on('stderr', (stderr) => {
    console.error("🔥 Python stderr:", stderr);
});

shell.on('error', (err) => {
    console.error("🔥 Python プロセスのエラー:", err);
});

shell.on('exit', (code) => {
    console.log(`🔚 Python プロセス終了: コード ${code}`);
});
