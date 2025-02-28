import json

# 以下のjson文字列はElectronからPythonにTCP通信を依頼する時に渡すデータの例です。

# ルーム作成依頼時
client_data = {
    "ip": "127.0.0.1",
    "port": 6058,
    "operation": 1,
    "type": "",
    "room_name": "roomA",
    "password": "abc"
}

# ルーム一覧取得依頼時
# client_data = {
#     "ip": "127.0.0.1",
#     "port": 6058,
#     "operation": 2,
#     "type": "GET",
#     "room_name": "",
#     "password": ""
# }

# ルーム参加依頼時
# client_data = {
#     "ip": "127.0.0.1",
#     "port": 6058,
#     "operation": 2,
#     "type": "JOIN",
#     "room_name": "roomA",
#     "password": "abc"
# }


# PythonからElectronに渡すデータは以下です。何も無いときは空文字が入っています。

# error_message: string
# token: string
# room_list(存在するルーム名のリスト): array


print(json.dumps(client_data))