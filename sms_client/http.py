from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class HTTPRequest:
    method: str
    path: str
    headers: Dict[str, str]
    body: Optional[bytes] = None

    @classmethod
    def to_bytes(cls) -> bytes:
        headers = "\r\n".join(f"{k}: {v}" for k, v in cls.headers.items())
        request = f"{cls.method} {cls.path} HTTP/1.1\r\n{headers}\r\n\r\n"
        if cls.body:
            request = request.encode() + cls.body
        return request.encode()


@dataclass
class HTTPResponse:
    status_code: int
    headers: Dict[str, str]
    body: bytes

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> "HTTPResponse":
        header_end = binary_data.find(b"\r\n\r\n")
        headers_part = binary_data[:header_end] if header_end != -1 else b""
        body = binary_data[header_end + 4:] if header_end != -1 else b""

        lines = headers_part.split(b"\r\n")
        status_line = lines[0].decode()
        status_code = int(status_line.split(" ")[1])
        headers = {}
        for line in lines[1:]:
            if line:
                key, value = line.decode().split(": ", 1)
                headers[key] = value
        return cls(status_code, headers, body)
