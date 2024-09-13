from pydantic import BaseModel


class Position(BaseModel):
    x: float
    y: float
    z: float


class Rotation(BaseModel):
    r: float
    p: float
    y: float


class Transform(BaseModel):
    position: Position
    rotation: Rotation
