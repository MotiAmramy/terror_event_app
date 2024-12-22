# from sqlalchemy import Integer, Column, String
# from sqlalchemy.orm import relationship
#
# from app.db.models import Base
#
#
# class AttackType(Base):
#     __tablename__ = 'attack_types'
#     # attacktype1 id
#     id = Column(Integer, primary_key=True)
#     # attacktype1_txt
#     name = Column(String, nullable=False)
#
#     events = relationship("Event", back_populates="attack_type")
#
#     def __repr__(self):
#         return f"<AttackType(id={self.id}, name='{self.name}')>"