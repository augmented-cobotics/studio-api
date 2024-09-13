from pydantic import BaseModel, Field

from .robot import Robot

class Manufacturer(BaseModel):
    id: str

    name: str
    
    webpage: str
    
    logo: str

    robots: list[Robot]