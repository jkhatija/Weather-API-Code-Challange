import cherrypy


class OpenAPIHandler:
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        openapi_doc = {
            "openapi": "3.0.0",
            "info": {
                "title": "Weather API",
                "version": "1.0.0",
            },
            "paths": {
                "/api_weather": {
                    "get": {
                        "summary": "Get weather data",
                        "parameters": [
                            {
                                "name": "station_id",
                                "in": "query",
                                "description": "ID of the weather station",
                                "schema": {
                                    "type": "string"
                                }
                            },
                            {
                                "name": "date",
                                "in": "query",
                                "description": "Date for weather data",
                                "schema": {
                                    "type": "string",
                                    "format": "date"
                                }
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Successful response",
                                "content": {
                                    "application/json": {
                                        "example": [
                                            {
                                                "station_id": "example",
                                                "date": "2023-01-01",
                                                "max_temp": 25.0,
                                                "min_temp": 15.0,
                                                "precipitation": 5.0,
                                            }
                                        ]
                                    }
                                },
                            },
                        },
                    },
                },
                "/api_weather_stats": {
                    "get": {
                        "summary": "Get weather statistics",
                        "parameters": [
                            {
                                "name": "station_id",
                                "in": "query",
                                "description": "ID of the weather station",
                                "schema": {
                                    "type": "string"
                                }
                            },
                            {
                                "name": "year",
                                "in": "query",
                                "description": "Year for weather data",
                                "schema": {
                                    "type": "string",
                                    "format": "year"
                                }
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Successful response",
                                "content": {
                                    "application/json": {
                                        "example": [
                                            {
                                                "station_id": "example",
                                                "year": "2023",
                                                "avg_max_temp": 25.0,
                                                "avg_min_temp": 15.0,
                                                "total_acc_precipitation": 5.0,
                                            }
                                        ]
                                    }
                                },
                            },
                        },
                    },
                },
            },
        }
        return openapi_doc
