from flask import Flask, request, session, render_template, url_for, request, redirect
from flask_restful import Resource, Api
from firebase import *
import json

app = Flask(__name__)
api = Api(app)

class ArduinoReportAPI(Resource):
    def get(self, id):
        return None

    def post(self, id):
        json_data = request.get_json()

        data = {
            'id': json_data.get('id'),
            'degree': json_data.get('temp'),
            'soil_humidity': json_data.get('soilMoisture'),
            'air_humidity': json_data.get('airHumidity')
        }

        post_health_report(data)

        return 'Success'

class TreesListAPI(Resource):
    def get(self, owner):
        json_data = get_trees(owner)
        return json.dumps(json_data)

    def post(self, owner):
        return get_trees(owner)

class TreesAPI(Resource):
    def get(self, id):
        json_data = get_tree(id)
        return json.dumps(json_data)

    def post(self, id):
        json_data = get_tree(id)
        return json.dumps(json_data)

class WorkersListAPI(Resource):
    def get(self, owner):
        json_data = get_workers(owner)
        return json.dumps(json_data)

    def post(self, owner):
        return get_workers(owner)

class WorkersAPI(Resource):
    def get(self, id):
        json_data = get_worker(id)
        return json.dumps(json_data)

    def post(self, id):
        json_data = get_worker(id)
        return json.dumps(json_data)


api.add_resource(ArduinoReportAPI, '/api/health-report/<id>')

api.add_resource(TreesListAPI, '/api/trees/<owner>')
api.add_resource(WorkersListAPI, '/api/workers/<owner>')

api.add_resource(TreesAPI, '/api/tree/<id>')
api.add_resource(WorkersAPI, '/api/worker/<id>')

if __name__ == '__main__':
    app.run(debug=True)
