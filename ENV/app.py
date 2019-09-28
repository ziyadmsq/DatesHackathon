from flask import Flask, request, session, render_template, url_for, request, redirect
from flask_restful import Resource, Api
from firebase import *
import json
import numpy as np
from flask import jsonify
import pickle

app = Flask(__name__)
api = Api(app)
# load the model
model = pickle.load(open('../AI-MACHINE-LEARNING-DEEP-LEARNING-IMAGE-RECOGNITION-COMPUTER-VISION/model.pkl','rb'))

@app.route('/api/model',methods=['POST'])
def predict():
    data = request.get_json(force=True)
    prediction = model.predict([[np.array(data['exp'])]])
    output = prediction[0]
    return jsonify(output)

class ArduinoReportAPI(Resource):
    def get(self, id):
        return None

    def post(self, id):
        json_data = request.get_json()

        data = {
            'id': id,
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
            harvest['date'] = harvest['date'].strftime('%Y/%m/%d')

        for pesticide in json_data['pesticide']:
            pesticide['date'] = pesticide['date'].strftime('%Y/%m/%d')

        for temp in json_data['temp']:
            temp['date'] = temp['date'].strftime('%Y/%m/%d')

        for water in json_data['water']:
            water['date'] = water['date'].strftime('%Y/%m/%d')

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
        json_data['latestSubmission'] = json_data['latestSubmission'].strftime('%Y/%m/%d')
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
