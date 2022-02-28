from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_mongoengine import MongoEngine 
from controllers.dicom_controller import DicomController

app = Flask(__name__)
api = Api(app)

app.config['MONGODB_SETTINGS'] = {
    "db": "DICOM_DB"
}

db = MongoEngine(app)
api.add_resource(DicomController, '/dicom')

if __name__ == '__main__':
    app.run(debug=False)