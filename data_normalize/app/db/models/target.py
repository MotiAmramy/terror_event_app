# from sqlalchemy import Integer, String, Column, ForeignKey, Text
# from sqlalchemy.orm import relationship
#
# from app.db.models import Base
#
#
#
#
#
# class Target(Base):
#     __tablename__ = 'targets_types'
#     # targtype1 id
#     id = Column(Integer, primary_key=True)
#     # targtype1_txt
#     type = Column(String, nullable=False)
#
#     events = relationship("Event", back_populates="weapon")
#
#     def __repr__(self):
#         return f"<Target(id='{self.id}, type='{self.type}')>"