from marshmallow import Schema, fields


class ReceivedData(Schema):
    SeriesInstanceUID = fields.Str()
    PatientName = fields.Str()
    PatientID = fields.Str()
    StudyInstanceUID = fields.Str()
    InstancesInSeries = fields.Int()
