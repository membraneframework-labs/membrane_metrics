from typing import NewType
from dataclasses import dataclass


TwitterBearerToken = NewType("TwitterBearerToken", str)


@dataclass
class TwitterContext:
    bearer_token: TwitterBearerToken
