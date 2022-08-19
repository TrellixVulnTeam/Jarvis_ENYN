from src.modules import ModuleWrapper


def handle(text: str, wrapper: ModuleWrapper) -> None:
    """
    if wrapper.user is not None:
        if not wrapper.user == 'Unknown':
            responses = ['Wenn mich nicht alles täuscht bist du {}',
                         'Ich glaube du bist {}',
                         'Soweit ich das sehen kann bist du {}']
            response = random.choice(responses)
            wrapper.say(response.format(wrapper.user))
            return
    responses = ['Das kann ich gerade leider nicht sehen',
                 'Das musst du aktuell leider selbst wissen',
                 'Entschuldige, aber das kann ich leider gerade nicht beurteilen']
    wrapper.say(random.choice(responses))"""
    wrapper.say(
        "Die Nutzererkennung ist leider derzeit in Arbeit, daher kann ich das noch nicht sagen."
    )


def isValid(text: str) -> bool:
    text = text.lower()
    if "wer" in text and "bin" in text and "ich" in text:
        return True
    if "wie" in text and "heiße" in text and "ich" in text:
        return True
