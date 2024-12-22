# from sqlalchemy import Integer, String, Column
# from sqlalchemy.orm import relationship
#
# from app.db.models import Base
#
# class Region(Base):
#     __tablename__ = 'regions'
#     id = Column(Integer, primary_key=True)
#     region_name = Column(String, nullable=False)
#
#     countries = relationship("Country", back_populates="region")
#
#     def __repr__(self):
#         return f"<Region(id={self.id}, name='{self.name}')>"