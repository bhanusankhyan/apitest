from flask import Flask, render_template, request, jsonify
from database_setup import Base, Data, Geojson
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine('postgresql+psycopg2://bhanu:bhanu@localhost/project')
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
session = DBsession()
DBsession.autoflush=True
app = Flask(__name__)
            # Interview Part-1

@app.route('/post_location', methods=['POST','GET'])
def locationsAPI():
  if request.method == 'GET':
      data = session.query(Data).all()
      return jsonify(locations=[loc.serialize for loc in data])
  if request.method == 'POST':
    try:
      location = request.get_json()
      location['key'] = "IN/"+location['key']
      k = location['key']
      key = session.query(Data).filter_by(key=k).first()
      locations = session.query(Data).filter_by(latitude = location['latitude']).filter_by(longitude=location['longitude']).first()
      if key != None:
          return jsonify(result = "Pin code Already Exists")
      if  locations != None:
          return jsonify(result ="Location already exists!")
      if key is None:
          new_location = Data(key = location['key'], place_name = location['place_name'], admin_name1 = location['admin_name1'], latitude = location['latitude'],longitude=location['longitude'])
      session.add(new_location)
      session.commit()
      return jsonify(result = "success!")
    except:
        session.rollback()
        return jsonify(result = "failure")

               #Interview Part-2 and Part-3

@app.route('/interview_2_3', methods=['POST','GET'])
def LocationRadius():
    if request.method == 'GET':
        return render_template('location.html')
    if request.method == 'POST':
      try:
        lat = request.form['latitude']
        lng = request.form['longitude']
        loc =session.execute("select * from geojson where latitude::TEXT like '{:s}%' and longitude::TEXT like '{:s}%';".format(lat,lng)).first()
        return jsonify (city = loc['city_name'], parent = loc.parent,latitude=lat,longitude=lng)
      except:
         return jsonify(result="Location does not exist in database")


@app.route('/get_using_postgres')
def CalUsingPostgres():
    if request.method == 'GET':
        lat = float(request.args.get("latitude"))
        lng = float(request.args.get("longitude"))
        rad = int(request.args.get("radius"))
        radius = rad*1000
        content = session.execute('select key,earth_distance(ll_to_earth({:f},{:f}),ll_to_earth(latitude,longitude)) as distance from locations where earth_box(ll_to_earth({:f},{:f}),{:d}) @> ll_to_earth(latitude,longitude);'.format(lat,lng,lat,lng,radius))
        distance= {}
        for c in content:
            distance.update({c.key:c.distance})
        return jsonify(result=distance)

@app.route('/get_using_self')
def CalUsingMath():
    if request.method == 'GET':
        lat = float(request.args.get('latitude'))
        lng = float(request.args.get('longitude'))
        rad = int(request.args.get('radius'))
        radius = rad*1000;
        distance = {}
        part1 = session.execute('create view distance as select key,(6371e3*(2* atan2(sqrt(sin(((latitude-{:f})*0.01745329252)/2)*sin(((latitude-{:f})*0.01745329252)/2)+cos({:f}*0.01745329252)*cos(latitude*0.01745329252)*sin(((longitude-{:f})*0.01745329252)/2)*sin(((longitude-{:f})*0.01745329252)/2)),sqrt(1-(sin(((latitude-{:f})*0.01745329252)/2)*sin(((latitude-{:f})*0.01745329252)/2)+cos({:f}*0.01745329252)*cos(latitude*0.01745329252)*sin(((longitude-{:f})*0.01745329252)/2)*sin(((longitude-{:f})*0.01745329252)/2)))))) as distance from locations; '.format(lat,lat,lat,lng,lng,lat,lat,lat,lng,lng))
        cont = session.execute("select * from distance where distance <= {:f};".format(radius))
        part2 = session.execute("drop view distance;")
        for c in cont:
            distance.update({c.key:c.distance})
        return jsonify(result = distance)















if __name__ == '__main__':
    app.debug =True
    app.run(host='0.0.0.0', port=8000)
