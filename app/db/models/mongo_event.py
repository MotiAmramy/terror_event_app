from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional




@dataclass
class Location:
    country: str
    region: Optional[str] = None
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    def to_dict(self):
        return {
            'region': self.region,
            'country': self.country,
            'city': self.city,
            'latitude': self.latitude,
            'longitude': self.longitude
        }




@dataclass
class TerrorEvent:
    date: datetime
    location: Location
    attack_types: Optional[List[str]]
    target_types: Optional[List[str]]
    group_types: Optional[List[str]]
    description: Optional[str] = None
    fatalities: Optional[int] = None
    injuries: Optional[int] = None
    casualties: Optional[int] = None
    num_of_attackers: Optional[int] = None

    def to_dict(self):
        return {
            'date': self.date,
            'description': self.description,
            'fatalities': self.fatalities,
            'injuries': self.injuries,
            'casualties': self.casualties,
            'num_of_attackers': self.num_of_attackers,
            'location': self.location.to_dict(),
            'attack_types': self.attack_types,
            'target_types': self.target_types,
            'group_types': self.group_types
        }
