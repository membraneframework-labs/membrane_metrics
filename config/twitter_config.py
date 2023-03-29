from typing import NewType
from dataclasses import dataclass


TwitterBearerToken = NewType("TwitterBearerToken", str)


@dataclass
class TwitterConfig:
    bearer_token: TwitterBearerToken
