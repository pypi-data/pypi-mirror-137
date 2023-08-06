from typing import List

from pydantic import BaseModel


class RethinkDBConfig(BaseModel):
    name: str = 'default'
    host: str = 'localhost'
    port: int = 28015
    password: str = None
    db: List[str] = []
