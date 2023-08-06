# RequestsWS
The Requests like WS module

# Installation
```
pip install requestsWS
```

# Usage
```python
import requestsWS

payload = {
    "message": "hello world!"
}
resp = requestsWS.post("wss://localhost:8765", identifiers={"message": "Hi there!"}, json=payload)
print(resp.text)

payload = {
    "method": "server.ping"
}
requestsWS.keepConnection('ws://localhost:8765', interval=20, json=payload)

payload = "hello world"
resp = requestsWS.post("ws://localhost:8765", data=payload)
print(resp.json())
```

# TO DO
   - Multiple connections at once (Use array instead of string)  
   - Add headers for opening connections  
   - Add support for identifiers that are deeper into the json  
   - Add string support for identifier (Check if identifier in string)

# Documentation
Coming soon!
