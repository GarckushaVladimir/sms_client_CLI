from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class HTTPRequest:
    method: str
    path: str
    headers: Dict[str, str]
    body: Optional[bytes] = None

    def to_bytes(self) -> bytes:
        headers = "\r\n".join(f"{k}: {v}" for k, v in self.headers.items())
        request = f"{self.method} {self.path} HTTP/1.1\r\n{headers}\r\n\r\n"
        if self.body:
            request = request.encode() + self.body
        return request


@dataclass
class HTTPResponse:
    status_code: int
    headers: Dict[str, str]
    body: bytes

    @classmethod
    def from_bytes(cls, binary_data: bytes) -> "HTTPResponse":
        try:
            header_end = binary_data.index(b"\r\n\r\n")
        except ValueError:
            header_end = len(binary_data)

        headers_part = binary_data[:header_end]
        body = binary_data[header_end + 4:]

        headers_lines = headers_part.split(b"\r\n")
        status_line = headers_lines[0].decode()
        proto, status_code, *reason = status_line.split(" ", 2)
        status_code = int(status_code)

        headers = {}
        for line in headers_lines[1:]:
            if line:
                key, value = line.decode().split(": ", 1)
                headers[key.strip()] = value.strip()

        return cls(status_code, headers, body)
