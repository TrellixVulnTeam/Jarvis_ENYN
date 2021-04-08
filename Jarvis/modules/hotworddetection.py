
def isValid(text):
	if 'hotworddetection' in text:
		return True
	
def handle(text, core, skills):
	room = core.analyze["room"]
	if room is None:
		room = core.room_name
			
	if 'start' in text: 
		core.change_hotworddetection(room=room, changing_to='on')
		core.say("Die Hotworddetection wurde eingeschaltet, ab jetzt höre ich wieder auf deine Komandos.", output='speech')
		core.say(f"Die Hotworddetection wurde im Raum {room} eingeschaltet.", output='messenger')
	elif 'stopp' in text:
		core.change_hotworddetection(room=room, changing_to='off')
		core.say("Die Hotworddetection wurde ausgeschaltet, ab jetzt höre ich nicht mehr auf deine Komandos.", output='speech')
		core.say(f"Die Hotworddetection wurde im Raum {room} ausgeschaltet, ab jetzt höre ich nicht mehr auf deine Komandos.", output='messenger')
		
