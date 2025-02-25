import json
import socket
import base64
from .config import Config
from .http import HTTPRequest, HTTPResponse


class SMSClient:
    def __init__(self, config: Config):
        self.config = config

    def send_sms(self, sender: str, recipient: str, message: str) -> HTTPResponse:
        body_data = {
            "sender": sender,
            "recipient": recipient,
            "message": message
        }
        body = json.dumps(body_data).encode()
        auth = base64.b64encode(f"{self.config.username}:{self.config.password}".encode()).decode()

        url = self.config.service_url.split("://")[-1]
        if ":" in url:
            host, port = url.split(":", 1)
        else:
            host = url
            port = 4010

        request = HTTPRequest(
            method="POST",
            path="/send_sms",
            headers={
                "Host": host,
                "Content-Type": "application/json",
                "Authorization": f"Basic {auth}",
                "Content-Length": str(len(body)),
            },
            body=body
        )

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, int(port)))
            sock.sendall(request.to_bytes())
            response_data = sock.recv(4096)

        response = HTTPResponse.from_bytes(response_data)
        return response
