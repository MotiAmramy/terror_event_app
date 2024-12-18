from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Location:
    region: str
    country: str
    province: str
    city: str
    latitude: Optional[float]
    longitude: Optional[float]


@dataclass
class Group:
    id: int
    name: str


@dataclass
class Attack:
    id: int
    name: str


@dataclass
class Target:
    id: int
    target: str
    target_type: str


@dataclass
class TerrorEvent:
    event_id: int
    date: datetime
    summary: str
    fatalities: int
    injuries: int
    casualties_number: int
    attackers_number: int
    location: Location
    attack_types: List[Attack] = field(default_factory=list)
    target_types: List[Target] = field(default_factory=list)
    group_types: List[Group] = field(default_factory=list)

