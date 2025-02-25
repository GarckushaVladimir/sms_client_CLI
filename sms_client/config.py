from dataclasses import dataclass

try:
    import tomllib  # Python 3.11+
except ImportError:
    import tomli as tomllib  # Python <3.11


@dataclass
class Config:
    service_url: str
    username: str
    password: str

    @classmethod
    def from_file(cls, path: str = "config.toml") -> "Config":
        with open(path, 'rb') as f:
            data = tomllib.load(f)
        return cls(**data["sms_service"])
