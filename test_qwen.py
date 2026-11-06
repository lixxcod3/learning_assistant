
import json
import urllib.request

url = "http://localhost:11434/api/generate"

data = {
    "model": "qwen2.5:3b",
    "prompt": "Explain what machine learning is in 3 simple sentences.",
    "stream": False
}

request = urllib.request.Request(
    url,
    data=json.dumps(data).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(request, timeout=120) as response:
        result = json.loads(response.read().decode("utf-8"))

    print("QWEN RESPONSE:")
    print(result["response"])

except Exception as e:
    print("ERROR:", e)
