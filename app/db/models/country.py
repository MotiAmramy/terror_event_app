# from sqlalchemy import Integer, String, Column, ForeignKey
# from sqlalchemy.orm import relationship
#
# from app.db.models import Base
#
#
#
# # Country Table
# class Country(Base):
#     __tablename__ = 'countries'
#     id = Column(Integer, primary_key=True)
#     country_name = Column(String, nullable=False)
#     region_id = Column(Integer, ForeignKey('regions.id'))
#
#     region = relationship("Region", back_populates="countries")
#     events = relationship("Event", back_populates="country")
#
#     def __repr__(self):
#         return f"<Country(id={self.id}, name='{self.name}', region_id={self.region_id})>"
