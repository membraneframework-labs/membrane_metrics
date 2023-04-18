from dataclasses import dataclass

@dataclass
class PlotsConfig:
    username: str
    password: str

    def get_authentication_dict(self) -> dict:
        return {self.username: self.password}
