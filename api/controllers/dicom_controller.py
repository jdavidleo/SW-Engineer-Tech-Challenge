import json
from flask import jsonify, request
from flask_restful import Resource
from marshmallow import ValidationError
from schemas.received_data_schema import ReceivedData as RecievedDataSchema
from data_access.models.received_data import ReceivedData as RecievedDataDAL


received_data_schema = RecievedDataSchema()


class DicomController(Resource):

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        # Validate and deserialize input
        try:
            data = received_data_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        RecievedDataDAL(SeriesInstanceUID=data['SeriesInstanceUID'],
                PatientName=data['PatientName'], PatientID=data['PatientID'],
                StudyInstanceUID=data['StudyInstanceUID'],
                InstancesInSeries=data['InstancesInSeries']).save()
        return "New object created"
    
    def get(self):
        all_objects = [json.loads(o.to_json()) for o in RecievedDataDAL.objects]
        count = len(all_objects)
        return {'objects':all_objects, 'count':count}
