# from sqlalchemy import Integer, String, Column, ForeignKey, Text
# from sqlalchemy.orm import relationship
#
# from app.db.models import Base
#
#
#
#
# class Group(Base):
#     __tablename__ = 'groups'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     motive = Column(Text)
#
#
#     events = relationship("Event", back_populates="group")
#
#     def __repr__(self):
#         return f"<Group(id={self.id}, name='{self.name}', motive='{self.motive}')>"
#
