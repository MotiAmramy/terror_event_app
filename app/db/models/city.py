# from app.db.models import Base
#
#
# class City(Base):
#     __tablename__ = 'cities'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String)
#
#     country_id = Column(Integer, ForeignKey('countries.id'))
#
#     def __repr__(self):
#         return f"<City(id={self.id}, name='{self.name}', region_id={self.region_id})>"