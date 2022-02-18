from Audio_Input import Test_Audio_Input
from Audio_Output import Test_Audio_Output
from Modules import Test_Modules


class Test_Core:
    def __init__(self):
        self.Audio_Output = Test_Audio_Output()
        self.Audio_Input = Test_Audio_Input()
        self.modules = Test_Modules()

    def start_module(self, text, name):
        print(f"Starting module '{name}' with text '{text}'")
        self.modules.start_module(None, text, name, False)
