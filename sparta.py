import requests

url = "http://127.0.0.1:8000/translate"
data = {
    "source_code": "print('Hello, World!')",
    "source_lang": "Python",
    "target_lang": "JavaScript"
}

response = requests.post(url, json=data)
print(response.json())  # This will print the translated code