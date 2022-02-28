import mongoengine as me


class ReceivedData(me.Document):
    SeriesInstanceUID = me.StringField(required=True)
    PatientName = me.StringField(required=True)
    PatientID = me.StringField(required=True)
    StudyInstanceUID = me.StringField(required=True)
    InstancesInSeries = me.IntField(required=True)
