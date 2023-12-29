import unittest
import requests
import cherrypy
from app import WeatherApp

class WeatherAppTest(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        # This method is called once at the beginning of the test suite
        cherrypy.tree.mount(WeatherApp())
        cherrypy.engine.start()

    @classmethod
    def tearDownClass(cls):
        # This method is called once at the end of the test suite
        cherrypy.engine.stop()
        
    @classmethod
    def start_cherrypy_server(cls):
        cherrypy.config.update({'server.socket_port': 8080}) 
        cherrypy.quickstart(WeatherApp())

    def test_api_weather(self):
        url = 'http://localhost:8080/api_weather'
        payload = {'date': '19850101','station_id':'USC00257715'}
        
        response = requests.get(url,params=payload)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsInstance(data, list)
        self.assertTrue(all(isinstance(entry, dict) for entry in data))

    def test_api_weather_stats(self):
        url = 'http://localhost:8080/api_weather_stats'
        payload = {'year': '1985','station_id': 'USC00110072'}

        response = requests.get(url, params=payload)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIsInstance(data, list)
        self.assertTrue(all(isinstance(entry, dict) for entry in data))

if __name__ == '__main__':
    unittest.main()