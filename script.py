import sys
import json

data = {"message": "Hello from Python!"}
print(json.dumps(data))  # JSON 形式で出力
sys.stdout.flush()
