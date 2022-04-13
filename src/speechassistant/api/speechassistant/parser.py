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

days_one_day_parser = reqparse.RequestParser()
days_one_day_parser.add_argument('id', type=int),
days_one_day_parser.add_argument('day', type=int),
days_one_day_parser.add_argument('month', type=int)

retakes_days_parser = reqparse.RequestParser()
retakes_days_parser.add_argument('monday', type=bool),
retakes_days_parser.add_argument('tuesday', type=bool),
retakes_days_parser.add_argument('wednesday', type=bool),
retakes_days_parser.add_argument('thursday', type=bool),
retakes_days_parser.add_argument('friday', type=bool),
retakes_days_parser.add_argument('saturday', type=bool),
retakes_days_parser.add_argument('sunday', type=bool),
retakes_days_parser.add_argument('date_of_day', type=list[days_one_day_parser],
                                 help='Date, when this routine should be active')

activation_time_parser = reqparse.RequestParser()
activation_time_parser.add_argument('id', type=int)
activation_time_parser.add_argument('hour', type=int)
activation_time_parser.add_argument('minute', type=int)

retakes_activation_parser = reqparse.RequestParser()
retakes_activation_parser.add_argument('clock_time', type=[activation_time_parser], help='Clock times, when this '
                                                                                         'routine should start')
retakes_activation_parser.add_argument('after_alarm', type=bool, help='Indicates, if the routine should start after '
                                                                      'an alarm at this day')
retakes_activation_parser.add_argument('after_sunrise', type=bool, help='Indicates, if the routine should start after '
                                                                        'sunrise at this day')
retakes_activation_parser.add_argument('after_sunset', type=bool, help='Indicates, if the routine should start after '
                                                                       'sunset at this day')
retakes_activation_parser.add_argument('after_call', type=bool, help='Indicates, if the routine should start after an '
                                                                     'user call at this day')

routine_retakes_parser = reqparse.RequestParser()
routine_retakes_parser.add_argument('days', type=retakes_days_parser)
routine_retakes_parser.add_argument('activation', type=activation_time_parser)

action_command_parser = reqparse.RequestParser()
action_command_parser.add_argument('id', type=int, help='ID of command')
action_command_parser.add_argument('module_name', type=str, help='Name of module, which will be called')
action_command_parser.add_argument('text', type=list[str], help='Text, with which the module will be called')

routine_action_parser = reqparse.RequestParser()
routine_action_parser.add_argument('commands', type=list[action_command_parser], help='Modules, which are called by '
                                                                                      'this routine')

routine_parser = reqparse.RequestParser()
routine_parser.add_argument('name', type=str, help='Name of the routine')
routine_parser.add_argument('descriptions', type=str,
                            help='A more detailed description of what the routine does exactly')
routine_parser.add_argument('on_commands', type=list[str], help='Commands (user says Jarvis, <command>), '
                                                                'on which this routine starts.')
routine_parser.add_argument('retakes', type=routine_retakes_parser)
routine_parser.add_argument('actions', type=routine_action_parser)

