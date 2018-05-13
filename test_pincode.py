from pincode import app
import json
import unittest

class FlaskTestCase(unittest.TestCase):
 # API for locations data in database

   def test_index(self):
      tester = app.test_client(self)
      response = tester.get('/post_location', content_type='html/text')
      self.assertEqual(response.status_code, 200)
 # Comparing Results Calculated Using Postgres and Mathematical Functions

   def test_checkLocation(self):
       self.maxDiff = None
       tester = app.test_client(self)
       response1 = tester.get('/get_using_postgres?latitude=28.6333&longitude=77.2167&radius=4',content_type='html/text')
       response2 = tester.get('/get_using_self?latitude=28.6333&longitude=77.2167&radius=4',content_type='html/text')
       self.assertEqual(json.loads(response1.data.decode('utf-8')), json.loads(response2.data.decode('utf-8')))

   def test_loc(self):
       tester = app.test_client(self)
      #  Adding New Location
       response1 = tester.post('/post_location',
                               data = (json.dumps({'key':'56','place_name':'unknown','admin_name1':'unknown','latitude':9532.224,'longitude':255.225})),
                               content_type = 'application/json')
       self.assertIn("success",str(response1.data))
        # Checking Previosly existing location
       response2 = tester.post('/post_location',
                                data = (json.dumps({'key':'110001','place_name':'Connaught Place','admin_name1':'New Delhi','latitude':28.6333,'longitude':77.2167})),
                                content_type = 'application/json')
       self.assertNotIn("success",str(response2.data))
 # Checking Location in Geojson Database File

   def test_location(self):
        tester = app.test_client(self)
        response = tester.post('/interview_2_3',
                               data = {'latitude':'77.055058','longitude':'28.524246'})
        self.assertNotIn('Location does not exist',str(response.data))

if __name__ == '__main__':
  unittest.main()
