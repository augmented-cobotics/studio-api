from pydantic import BaseModel, Field

from .transform import *
from enum import Enum

from typing import Optional, List, ForwardRef

#
#
#

class RobotDescriptionLinkVisuals(BaseModel):
    origin: Transform
    mesh: str

class RobotDescriptionLinkCollisions(BaseModel):
    origin: Transform
    mesh: str


class RobotDescriptionLink(BaseModel):
    visuals: Optional[RobotDescriptionLinkVisuals] = None
    collisions: Optional[RobotDescriptionLinkCollisions] = None
    joints: List['RobotDescriptionJoint']
    
#
#
#

class RobotDescriptionJointType(str, Enum):
    fixed = "fixed"
    revolute = "revolute"


class RobotDescriptionJointLimits(BaseModel):
    effort: float
    lower: float
    upper: float
    velocity: float


class RobotDescriptionJoint(BaseModel):
    name: str
    type: RobotDescriptionJointType
    origin: Transform
    axis: Optional[Position] = None
    limits: Optional[RobotDescriptionJointLimits] = None
    link: RobotDescriptionLink

#
#
#

class RobotDescription(BaseModel):
    root: RobotDescriptionLink

#
#
#

class RobotSpecs(BaseModel):
    reach: int

    payload: float

    dof: int

    repeatability: float

    weight: float


class Robot(BaseModel):
    id: str

    name: str

    description: str

    content: str

    webpage: str

    avatar: str

    banner: str

    specs: RobotSpecs
    
    tree: Optional[RobotDescription] = Field(default=[], exclude=True)
