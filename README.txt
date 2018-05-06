This Project 'apitest' is created using Python 3.6, flask, Postgres, SQLAlchemy, psycopg2
1. Add these files at a particular location.
2. Create User 'bhanu' with password 'bhanu' in postgresql database.
3. Create database 'project' and give user 'bhanu' its privileges.
3. Run the 'database_setup.py' file, to create tables in database.
4. Import data from 'IN.csv' into your database
5. Run geojson_setup.py file, to import data from 'data.json' file into your database.
6. Run pincode.py file in order to execute project.
7. Open any browser.
8. For Interview Phase-1, visit "http://localhost:8000/post_location" for GET request.
9. To access POST request, send a POST request on "http://localhost:8000/post_location" using parameters ["key":"<<value>>","place_name":"<<value>>","admin_name1":"<<value>>","latitude":"<<value>>","longitude":"<<value>>"] and headers "contect-type:application/json" 
10. Interview Phase-2 and Phase-3 are at endpoint "http://localhost:8000/intervie_2_3"

