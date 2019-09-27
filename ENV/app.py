from flask import Flask, request, session, render_template, url_for, request, redirect
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

class DatesHealth(Resource):
    def get(self):
        return None

    def post(self):
        return None

api.add_resource(DatesHealth, '/health-report')

if __name__ == '__main__':
    app.run(debug=True)
