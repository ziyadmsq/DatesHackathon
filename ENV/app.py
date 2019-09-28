from flask import Flask, request, session, render_template, url_for, request, redirect
from flask_restful import Resource, Api
from firebase import *
import json
import numpy as np
import cv2
from flask import jsonify
from sklearn.preprocessing import LabelEncoder
from PIL import Image
import pickle

app = Flask(__name__)
api = Api(app)
# load the model
model = pickle.load(open('../AI-MACHINE-LEARNING-DEEP-LEARNING-IMAGE-RECOGNITION-COMPUTER-VISION/model.pkl','rb'))

def quantify_image(image):
    features = feature.hog(image, orientations=9,
        pixels_per_cell=(10, 10), cells_per_block=(2, 2),
        transform_sqrt=True, block_norm="L1")

    return features

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

class PredictionAPI(Resource):
    def get(self):
        return None

    def post(self):
        image = Image.open(request.files['file'])
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (200, 200))
        image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        features = quantify_image(image)

        prediction = model.predict(features)
        output = prediction[0]
        return jsonify(output)

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

class RecentAPI(Resource):
    def get(self, owner):
        json_data = get_recent(owner)
        return json.dumps(json_data)

    def post(self, owner):
        None


api.add_resource(ArduinoReportAPI, '/api/health-report/<id>')

api.add_resource(TreesListAPI, '/api/trees/<owner>')
api.add_resource(WorkersListAPI, '/api/workers/<owner>')

api.add_resource(TreesAPI, '/api/tree/<id>')
api.add_resource(WorkersAPI, '/api/worker/<id>')

api.add_resource(RecentAPI, '/api/recent/<owner>')

api.add_resource(PredictionAPI, '/api/model')

if __name__ == '__main__':
    app.run(debug=True)
