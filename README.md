# Desktop-Chat-Messenger
### おおまかな流れ
1. ユーザーが **ボタンをクリック**
2. **Electron が Python を実行**
3. Python が **JSON データを出力**
4. **Electron が受け取り、UI に表示**

## Electron アプリを実行
```bash
npm start
```

## **📂 ディレクトリ構造**

```
my-electron-app/
│── 📄 package.json        # プロジェクト設定
│── 📄 main.js             # Electron メインプロセス
│── 📄 renderer.js         # フロントエンド（レンダラープロセス）
│── 📄 index.html          # フロントエンド UI
│── 📄 script.py           # Python スクリプト
└── 📂 node_modules/       # npm の依存ファイル
```
### **📌 各ファイルの役割**

| ファイル/フォルダ | 説明 |
| --- | --- |
| `package.json` | npm パッケージ管理、Electron の起動スクリプト設定 |
| `main.js` | Electron のメインプロセス（ウィンドウの作成 & Python 実行） |
| `renderer.js` | UI から Python を実行するための IPC 通信を担当 |
| `index.html` | フロントエンドの UI |
| `script.py` | Python スクリプト（Electron から実行するコード） |

### pythonのテスト方法
#### ライブラリのインストール
```
python3 -m venv my_env
source my_env/bin/activate
pip install -r requirements.txt
```
#### TCP接続（ルームの作成、ルーム一覧の取得、ルームの参加）
以下のコマンドを実行することで、tcp_client_test_data.pyの標準出力がtcp_client.pyの標準入力に設定される。これを応用してElectrionからpythonを実行させたい。

```
python3 tcp_client_test_data.py | python3 tcp_client.py
```