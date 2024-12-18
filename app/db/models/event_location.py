# from sqlalchemy import String, Column, Float, column, ForeignKey, Integer
#
#
# class EventLocation:
#     __tablename__ = 'locations_events'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     city_name = Column(String)
#     latitude = Column(Float)
#     longitude = Column(Float)
#     city_id = Column(Integer, ForeignKey('cities.id'))
#
#
#
#     def __repr__(self):
#         return (f"<EventLocation(id={self.id}, city_name='{self.city_name}'"
#                 f", latitude={self.latitude}"
#                 f", longitude={self.longitude},"
#                 f"city_id{self.city_id})>")
