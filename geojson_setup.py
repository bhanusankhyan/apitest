from sqlalchemy import create_engine
from database_setup import Base, Geojson
from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker
import json
engine = create_engine("postgresql+psycopg2://bhanu:bhanu@localhost/project")
Base.metadata.bind =engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
with open('data.json','r') as f:
    data = json.load(f)
length = len(data['features'])
print ()
print(length)
for i in range(length):

        city = data['features'][i]['properties']['name']
        parent = data['features'][i]['properties']['parent']
        length2 = len(data['features'][i]['geometry']['coordinates'][0])
        for j in range(length2):
           lat = data['features'][i]['geometry']['coordinates'][0][j][0]
           lng = data['features'][i]['geometry']['coordinates'][0][j][1]
           new_location = Geojson(city_name = city, parent = parent, latitude = lat, longitude = lng)
           session.add(new_location)
           session.commit()
           print('In progress')
print('completed')
