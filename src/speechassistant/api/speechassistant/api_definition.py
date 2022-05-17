from flask_restx import fields
from src.speechassistant.api.myapi import api

service = api.model(
    "Service",
    {
        "name": fields.String(
            readOnly=True, description="Name of the service you want to access"
        )
    },
)

audio_file = api.model(
    "AudioFile",
    {
        "name": fields.String(description="Name of audio file under which it is saved"),
        "old_name": fields.String(
            description="Name of audio file which should be renamed"
        ),
    },
)

alarm_file = api.model(
    "Alarm",
    {
        "id": fields.Integer(description="ID of the alarm"),
        "time": fields.String,
        "repeating": fields.String,
        "sound": fields.String(
            default="standard.wav",
            description="Name of the audio file which is played on alarm",
        ),
        "user": fields.Integer(
            default=-1,
            description='ID of the user, who "owns" the alarm. If ID=-1, the alarm is not '
            "owned by anyone",
        ),
        "text": fields.String(description="Text which is said on alarm"),
        "active": fields.Boolean(description="Indicates if the alarm is active"),
        "initiated": fields.Boolean(
            readonly=True,
            description="Indicates if the sunrise function was started yet",
        ),
        "last_executed": fields.String(
            readonly=True, description="Date-string of last activation (DD.MM.YYYY)"
        ),
    },
)

time = api.inherit(
    "time",
    alarm_file,
    {
        "hour": fields.Integer(description="Hour of activation time"),
        "minute": fields.Integer(description="Minute of activation time"),
        "total_seconds": fields.Integer(
            readOnly=True, description="= hour*3600 + minute*60"
        ),
    },
)

repeating = api.inherit(
    "repeating",
    alarm_file,
    {
        "monday": fields.Boolean(
            description="Indicates if the alarm is activated on monday"
        ),
        "tuesday": fields.Boolean(
            description="Indicates if the alarm is activated on tuesday"
        ),
        "wednesday": fields.Boolean(
            description="Indicates if the alarm is activated on wednesday"
        ),
        "thursday": fields.Boolean(
            description="Indicates if the alarm is activated on thursday"
        ),
        "friday": fields.Boolean(
            description="Indicates if the alarm is activated on friday"
        ),
        "saturday": fields.Boolean(
            description="Indicates if the alarm is activated on saturday"
        ),
        "sunday": fields.Boolean(
            description="Indicates if the alarm is activated on sunday"
        ),
    },
)

routine = api.model(
    "Routine",
    {
        "name": fields.String(description="Name of the routine"),
        "description": fields.String(
            description="A more detailed description of what the routine does exactly"
        ),
        "on_commands": fields.List(
            fields.String(),
            description="Commands (user says Jarvis, <command>), "
            "on which this routine starts.",
        ),
        "retakes": fields.String,
        "actions": fields.String,
    },
)

retakes = api.inherit(
    "retakes", routine, {"days": fields.String, "activation": fields.String}
)

one_date = api.inherit(
    "one_date",
    {"id": fields.Integer(), "day": fields.Integer(), "month": fields.Integer()},
)

days = api.inherit(
    "days",
    retakes,
    {
        "monday": fields.Boolean(),
        "tuesday": fields.Boolean(),
        "wednesday": fields.Boolean(),
        "thursday": fields.Boolean(),
        "friday": fields.Boolean(),
        "saturday": fields.Boolean(),
        "sunday": fields.Boolean(),
        "date_of_day": fields.List(
            fields.Nested(one_date),
            description="Date, when this routine should be active",
        ),
    },
)

routine_time = api.inherit(
    "time",
    retakes,
    {"id": fields.Integer(), "hour": fields.Integer(), "minute": fields.Integer()},
)

activation = api.inherit(
    "activation",
    retakes,
    {
        "clock_time": fields.List(
            fields.Nested(routine_time),
            description="Clock times, when this routine should start",
        ),
        "after_alarm": fields.Boolean(
            description="Indicates, if the routine should start after an alarm at this day"
        ),
        "after_sunrise": fields.Boolean(
            description="Indicates, if the routine should start after sunrise at this day"
        ),
        "after_sunset": fields.Boolean(
            description="Indicates, if the routine should start after sunset at this day"
        ),
        "after_call": fields.Boolean(
            description="Indicates, if the routine should start after an user call at this day"
        ),
    },
)

one_command = api.inherit(
    "command",
    {
        "id": fields.Integer(description="ID of command"),
        "module_name": fields.String(
            description="Name of module, which will be called"
        ),
        "text": fields.List(
            fields.String(), description="Text, with which the module will be called"
        ),
    },
)

actions = api.inherit(
    "actions",
    retakes,
    {
        "commands": fields.List(
            fields.Nested(one_command),
            description="Modules, which are called by this routine",
        )
    },
)
