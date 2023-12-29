import cherrypy
import json,os
from sqlalchemy import create_engine, text
from swagger_ui_bundle import swagger_ui_path
from openapi_handler import OpenAPIHandler
engine = create_engine('sqlite:///weather.db', echo=True)


class WeatherApp:


    @cherrypy.expose
    def index(self):
        return None

    @cherrypy.expose
    @cherrypy.tools.json_out()

    def api_weather(self, date=None, station_id=None, page=1, size=10):
        offset = (int(page) - 1) * int(size)
        query = "SELECT * FROM weather_records"
        filters = []
        if date:
            filters.append(f"Date == '{date}'")
        if station_id:
            filters.append(f"Station_ID== '{station_id}'")
        if filters:
            query += " WHERE " + " AND ".join(filters)
        query += f" LIMIT {size} OFFSET {offset}"

        with engine.connect() as conn:
            result = conn.execute(text(query))
            rows = result.fetchall()

        if not rows:
            raise cherrypy.HTTPError(404, "No data found for the specified dates")

        weather_data = []
        for row in rows:
            weather_data.append({
                "station_id": row[5],
                "date": row[1],
                "max_temp": row[2],
                "min_temp": row[3],
                "precipitaion": row[4],
            })

        return weather_data

    @cherrypy.expose
    @cherrypy.tools.json_out()

    def api_weather_stats(self, year=None, station_id=None, page=1, size=10):
        offset = (int(page) - 1) * int(size)
        query = "SELECT * FROM weather_stats"
        filters = []
        if year:
            filters.append(f"Date == '{year}'")
        if station_id:
            filters.append(f"Station_ID== '{station_id}'")
        if filters:
            query += " WHERE " + " AND ".join(filters)
        query += f" LIMIT {size} OFFSET {offset}"

        with engine.connect() as conn:
            result = conn.execute(text(query))
            rows = result.fetchall()

        if not rows:
            raise cherrypy.HTTPError(404, "No data found for the specified dates")

        weather_data = []
        for row in rows:
            weather_data.append({
                "station_id": row[1],
                "date": row[2],
                "avg_max_temp": row[3],
                "avg_min_temp": row[4],
                "total_acc_precipitation": row[5]
            })

        return weather_data



if __name__ == '__main__':

    conf= {
    '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
    '/openapi.json': {
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
        },
    '/swaggerui': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './swagger_ui_dist',
        },
    }
    config = {
    '/swagger': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': swagger_ui_path,
            'tools.staticdir.index': 'index.html',
        },

    }

    cherrypy.tree.mount(OpenAPIHandler(), '/openapi.json', conf)

    cherrypy.tree.mount(WeatherApp(), '/',config=config)
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.engine.start()
    cherrypy.engine.block()