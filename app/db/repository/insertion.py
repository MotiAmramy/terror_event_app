# from sqlalchemy.exc import SQLAlchemyError
# from app.db.models.attack_type import AttackType
# from app.db.models.country import Country
# from app.db.models.event import Event
# from app.db.models.group import Group
# from app.db.models.region import Region
# from app.db.models.target import Weapon

#
#
#
#
# def insert_region(session, name):
#     try:
#         region = Region(name=name)
#         session.add(region)
#         session.commit()
#         print(f"Inserted: {region}")
#     except SQLAlchemyError as e:
#         session.rollback()
#         print(f"Error inserting region: {e}")
#
# def insert_country(session, name, region_id):
#     try:
#         country = Country(name=name, region_id=region_id)
#         session.add(country)
#         session.commit()
#         print(f"Inserted: {country}")
#     except SQLAlchemyError as e:
#         session.rollback()
#         print(f"Error inserting country: {e}")
#
#
# def insert_event(session, year, month, day, city, latitude, longitude, summary, fatalities, injuries, country_id, attack_type_id, group_id, weapon_id):
#     try:
#         event = Event(
#             year=year,
#             month=month,
#             day=day,
#             city=city,
#             latitude=latitude,
#             longitude=longitude,
#             summary=summary,
#             fatalities=fatalities,
#             injuries=injuries,
#             country_id=country_id,
#             attack_type_id=attack_type_id,
#             group_id=group_id,
#             weapon_id=weapon_id
#         )
#         session.add(event)
#         session.commit()
#         print(f"Inserted: {event}")
#     except SQLAlchemyError as e:
#         session.rollback()
#         print(f"Error inserting event: {e}")
#
#
# def insert_attack_type(session, name):
#     try:
#         attack_type = AttackType(name=name)
#         session.add(attack_type)
#         session.commit()
#         print(f"Inserted: {attack_type}")
#     except SQLAlchemyError as e:
#         session.rollback()
#         print(f"Error inserting attack type: {e}")
#
#
# def insert_group(session, name, motive):
#     try:
#         group = Group(name=name, motive=motive)
#         session.add(group)
#         session.commit()
#         print(f"Inserted: {group}")
#     except SQLAlchemyError as e:
#         session.rollback()
#         print(f"Error inserting group: {e}")
#
# def insert_weapon(session, weapon_type, description):
#     try:
#         weapon = Weapon(type=weapon_type, description=description)
#         session.add(weapon)
#         session.commit()
#         print(f"Inserted: {weapon}")
#     except SQLAlchemyError as e:
#         session.rollback()
#         print(f"Error inserting weapon: {e}")