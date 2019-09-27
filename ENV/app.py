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
        None

class TreesAPI(Resource):
    def get(self, id):
        json_data = get_tree(id)

        for harvest in json_data['harvest']:
            harvest['date'] = harvest['date'].strftime('%m/%d/%Y')

        for pesticide in json_data['pesticide']:
            pesticide['date'] = pesticide['date'].strftime('%m/%d/%Y')

        for temp in json_data['temp']:
            temp['date'] = temp['date'].strftime('%m/%d/%Y')

        for water in json_data['water']:
            water['date'] = water['date'].strftime('%m/%d/%Y')

        return json.dumps(json_data)

    def post(self, id):
        None

class WorkersListAPI(Resource):
    def get(self, owner):
        json_data = get_workers(owner)
        return json.dumps(json_data)

    def post(self, owner):
        None

class WorkersAPI(Resource):
    def get(self, id):
        json_data = get_worker(id)
        json_data['latestSubmission'] = json_data['latestSubmission'].strftime('%m/%d/%Y')
        return json.dumps(json_data)

    def post(self, id):
        None


api.add_resource(ArduinoReportAPI, '/api/health-report/<id>')

api.add_resource(TreesListAPI, '/api/trees/<owner>')
api.add_resource(WorkersListAPI, '/api/workers/<owner>')

api.add_resource(TreesAPI, '/api/tree/<id>')
api.add_resource(WorkersAPI, '/api/worker/<id>')

if __name__ == '__main__':
    app.run(debug=True)
