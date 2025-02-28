import socket
from modules import TCPProtocolHandler
import json
import sys

# ★クラス毎の役割と連携
# 【役割】
# TCPProtocolHandler:TCPデータの作成、パース
# UDPProtocolHandler:UDPデータの作成、パース
# ChatClient:ユーザーインターフェースを提供し、ルームの作成、参加、チャット開始などの操作を処理
# TCPClient:TCP通信でのデータの送受信
# UDPClient:UDP通信でのデータの送受信
# 【連携】
# ChatClientでユーザーの要求を受信→TCP/UDPProtocolHandlerで送信データの作成→TCP/UDPClientでデータの送信と受信→TCP/UDPProtocolHandlerで受信データの解析→ChatClientでユーザーにデータ表示

# TCP通信でのデータの送受信
class TCPClient:
  def __init__(self, server_ip, tcp_port):
    self.server_address = (server_ip, tcp_port)
    self.sock = None

  # 役割：サーバーへの接続
  # 戻り値：真偽値（既に接続されている場合、または接続が成功した場合にTrueを返す。接続に失敗したらFalseを返す。）
  def connect(self):
    if self.sock:
      return True
    
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.settimeout(2)
    try:
      self.sock.connect(self.server_address)
      print("TCP接続されました。")
      return True
    except socket.error as e:
      return False
    
  # 役割：サーバーからのレスポンスを取得
  # 戻り値：レスポンスデータ
  def recieve_response(self):
      try:
        recieved_header_data = b""
        while len(recieved_header_data) < 32:
          chunk = self.sock.recv(32 - len(recieved_header_data))
          recieved_header_data += chunk

        room_name_size = recieved_header_data[0]
        operation_payload_size = int.from_bytes(recieved_header_data[3:], "big")
        total_body_size = room_name_size + operation_payload_size
        
        recieved_body_data = b""
        while len(recieved_body_data) < total_body_size:
          chunk = self.sock.recv(total_body_size - len(recieved_body_data))
          recieved_body_data += chunk
        
        response = recieved_header_data + recieved_body_data
        return response
      except socket.timeout as e:
        print(e)
      except socket.error as e:
        print(e)
    
  # 役割：サーバーへリクエストを送信
  # 戻り値：レスポンスデータ
  def send_request(self, request):
    try:
      self.sock.sendall(request)

      response = self.recieve_response()
      parsed_response = TCPProtocolHandler.parse_data(response)["operation_payload"]
      if parsed_response["error_message"]:
        return parsed_response

      response = self.recieve_response()
      parsed_response = TCPProtocolHandler.parse_data(response)["operation_payload"]
      return parsed_response
    except socket.timeout as e:
      print(e)
    except socket.error as e:
      print(e)

  # 役割：サーバーとの接続を解除する
  # 戻り値：無し
  def disconnect(self):
    if not self.sock:
      return
    self.sock.close()
    self.sock = None
    print("TCP接続を解除しました。")


# ユーザーインターフェースを提供し、ルームの作成、参加、チャット開始などの操作を処理。
class ChatClient:
  def __init__(self, tcp_client, udp_client):
    self.tcp_client = tcp_client
    self.udp_client = udp_client
    self.user_name = None
    self.room_token = () # (room, token)

 # 役割：Electron側から依頼されたリクエストを処理する
class ChatClient:
  def __init__(self, tcp_client):
    self.tcp_client = tcp_client

  def make_data(self, error_message="", token="", room_list=""):
    data = {
      "error_message": error_message,
      "token": token,
      "room_list": room_list
    }

    return json.dumps(data)

  # 役割：Electron側からの依頼(TCPサーバーにルームの作成やルーム一覧取得、ルームの参加)を実行し、そのレスポンス結果を出力する。
  # 戻り値：無し
  def exec(self, operation, type, room_name, password):
    try:
        if not self.tcp_client.connect():
            print(self.make_data(error_message="can not connect server"))

        if operation == 1:
            # ルーム作成依頼
            token, error_message = self.create_room_request(room_name=room_name, password=password)
            # print("以下のデータをElectron側で取得します。")
            print(self.make_data(token=token, error_message=error_message))

        elif operation == 2 and type == "GET":
            # ルーム一覧取得依頼
            room_list, error_message = self.get_room_list_request()
            # print("以下のデータをElectron側で取得します。")
            print(self.make_data(room_list=room_list, error_message=error_message))
            
        elif operation == 2 and type == "JOIN":
            # ルーム参加依頼
            token, error_message = self.join_room_request(room_name=room_name, password=password)
            # print("以下のデータをElectron側で取得します。")
            print(self.make_data(token=token, error_message=error_message))
    except Exception as e:
      print(self.make_data(error_message="unexpected error"))
    finally:
      self.tcp_client.disconnect()
      # print("disconnect tcp connection")
  # 役割：ルーム作成
  # 戻り値：成功=(トークン,None), 失敗=(None,エラーメッセージ)
  def create_room_request(self, room_name, password):
    # リクエストの作成
    request = TCPProtocolHandler.make_create_room_request(room_name, password)
    if not request:
      return None, "送信できるデータサイズを超過しています。"
    # サーバーにルーム作成依頼
    response = self.tcp_client.send_request(request)
    
    if not response:
      return None, "エラーが発生しました。"
    if response["error_message"]:
      return None, response["error_message"]
    else:
      self.room_token = (room_name, response["token"])
      return response["token"], None

  # 役割：ルーム一覧取得
  # 戻り値：成功=(ルーム一覧,None), 失敗=(None,エラーメッセージ)
  def get_room_list_request(self):
    # リクエストの作成
    request = TCPProtocolHandler.make_get_room_list_request()
    # サーバーにルーム一覧取得依頼
    response = self.tcp_client.send_request(request)

    if response is None:
      return None, "エラーが発生しました。"
    elif response["error_message"]:
      return None, response["error_message"]
    else:
      return response["room_list"], None

  # 役割：ルーム参加
  # 戻り値：成功=(トークン,None)、失敗=(None,エラーメッセージ)
  def join_room_request(self, room_name, password):
    # リクエストの作成
    request = TCPProtocolHandler.make_join_room_request(room_name, password)
    # サーバーにルーム参加依頼
    response = self.tcp_client.send_request(request)

    if response is None:
      return None, "エラーが発生しました。"
    if response["error_message"]:
      return None, response["error_message"]
    else:
      self.room_token = (room_name, response["token"])
      return response["token"], None



if __name__ == "__main__":
    data = sys.stdin.read()
    # print("\n以下のデータをElectron側から取得します")
    print(data)
    ip, port, operation, type, room_name, password = json.loads(data).values()
    # Electron側から渡されるデータ
    # - ip
    # - port
    # - operation(1=ルーム作成、2=ルーム一覧取得またはルーム参加)
    # - type(GET=ルーム一覧取得、JOIN=ルーム参加)
    # - room_name
    # - password

    # Electronに渡すデータ
    # error_message
    # token
    # room_list(存在するルーム名のリスト)

    tcp_client = TCPClient(ip, port)

    chat_client = ChatClient(tcp_client)

    chat_client.exec(operation, type, room_name, password)