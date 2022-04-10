from flask_restx import reqparse

audio_file_parser = reqparse.RequestParser()
audio_file_parser.add_argument('name', type=str, required=False, help='Name of a specific audio file')
audio_file_parser.add_argument('old_name', type=str, required=False,
                               help='Name of a specific audio file which should be changed')

alarm_parser = reqparse.RequestParser()
alarm_parser.add_argument('id', type=str, required=True, default=-1,
                          help='ID of alarm. If id is -1, all alarms are meant')
alarm_parser.add_argument('time', type=dict[[str, int], [str, int], [str, int]],
                          help='Activation-time of the alarm')
alarm_parser.add_argument('sound', type=str, help='Name of the audio file which is played on alar')
alarm_parser.add_argument('user', type=int, help='ID of the user, who "owns" the alarm')
alarm_parser.add_argument('text', type=str, help='Text which is said on alarm')
alarm_parser.add_argument('active', type=bool, help='Indicates if the alarm is active')
alarm_parser.add_argument('initiated', type=bool, help='Indicates if the sunrise function was started yet')
alarm_parser.add_argument('last_executed', type=str, help='Date-string of last activation (DD.MM.YYYY)')
