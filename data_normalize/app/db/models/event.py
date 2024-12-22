# from sqlalchemy import Integer, String, Column, ForeignKey, Float, Text
# from sqlalchemy.orm import relationship
#
# from app.db.models import Base
#
#
#
# class Event(Base):
#     __tablename__ = 'events'
#     id = Column(Integer, primary_key=True)
#     year = Column(Integer, nullable=False)
#     month = Column(Integer)
#     day = Column(Integer)
#     summary = Column(Text)
#     fatalities = Column(Integer, default=0)
#     injuries = Column(Integer, default=0)
#     casualties_number = Column(Integer, default=0)
#     attackers_number = Column(Integer, nullable=False)
#     location_id = Column(Integer, ForeignKey('locations_events.id'))
#     attack_type_id = Column(Integer, ForeignKey('attack_types.id'))
#     group_id = Column(Integer, ForeignKey('groups.id'))
#     weapon_id = Column(Integer, ForeignKey('weapons.id'))
#
#     country = relationship("Country", back_populates="events")
#     attack_type = relationship("AttackType", back_populates="events")
#     group = relationship("Group", back_populates="events")
#     weapon = relationship("Weapon", back_populates="events")
#
#     def __repr__(self):
#         return (
#             f"<Event(id={self.id}, year={self.year}, month={self.month}, day={self.day}, "
#             f"city='{self.city}', latitude={self.latitude}, longitude={self.longitude}, "
#             f"fatalities={self.fatalities}, injuries={self.injuries}, "
#             f"country_id={self.country_id}, attack_type_id={self.attack_type_id}, "
#             f"group_id={self.group_id}, weapon_id={self.weapon_id})>"
#         )
