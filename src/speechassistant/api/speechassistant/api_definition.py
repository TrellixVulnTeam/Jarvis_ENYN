from flask_restx import fields
from src.speechassistant.api.myapi import api

service = api.model('Service', {
    'name': fields.String(readOnly=True, description='Name of the service you want to access')
})

audio_file = api.model('AudioFile', {
    'name': fields.String(description='Name of audio file under which it is saved'),
    'old_name': fields.String(description='Name of audio file which should be renamed')
})

alarm_file = api.model('Alarm', {
    'id': fields.Integer(description='ID of the alarm'),
    'time': fields.String,
    'repeating': fields.String,
    'sound': fields.String(default='standard.wav', description='Name of the audio file which is played on alarm'),
    'user': fields.Integer(default=-1, description='ID of the user, who "owns" the alarm. If ID=-1, the alarm is not '
                                                   'owned by anyone'),
    'text': fields.String(description='Text which is said on alarm'),
    'active': fields.Boolean(description='Indicates if the alarm is active'),
    'initiated': fields.Boolean(readonly=True, description='Indicates if the sunrise function was started yet'),
    'last_executed': fields.String(readonly=True, description='Date-string of last activation (DD.MM.YYYY)')
})

time = api.inherit('Time', alarm_file, {
    'hour': fields.Integer(description='Hour of activation time'),
    'minute': fields.Integer(description='Minute of activation time'),
    'total_seconds': fields.Integer(readOnly=True, description='= hour*3600 + minute*60')
})

repeating = api.inherit('Reapeating', alarm_file, {
    'monday': fields.Boolean(description='Indicates if the alarm is activated on monday'),
    'tuesday': fields.Boolean(description='Indicates if the alarm is activated on tuesday'),
    'wednesday': fields.Boolean(description='Indicates if the alarm is activated on wednesday'),
    'thursday': fields.Boolean(description='Indicates if the alarm is activated on thursday'),
    'friday': fields.Boolean(description='Indicates if the alarm is activated on friday'),
    'saturday': fields.Boolean(description='Indicates if the alarm is activated on saturday'),
    'sunday': fields.Boolean(description='Indicates if the alarm is activated on sunday')
})


