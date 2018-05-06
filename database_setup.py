from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
Base = declarative_base()

class Data(Base):
    __tablename__ = 'locations'
    key = Column(String(10), primary_key = True)
    place_name = Column(String(40))
    admin_name1 = Column(String(40))
    latitude = Column(Float)
    longitude = Column(Float)
    accuracy = Column(Integer)

    @property
    def serialize(self):
        return{
    'key' : self.key,
    'place_name' : self.place_name,
    'admin_name1' : self.admin_name1,
    'latitude' : self.latitude,
    'longitude' : self.longitude,
    'accuracy' : self.accuracy,
    }
class Geojson(Base):
    __tablename__ = 'geojson'
    id = Column(Integer, autoincrement = True, primary_key=True)
    city_name = Column(String(30))
    parent = Column(String(30))
    latitude = Column(Float)
    longitude = Column(Float)


engine = create_engine('postgresql+psycopg2://bhanu:bhanu@localhost/project')
Base.metadata.create_all(engine)
