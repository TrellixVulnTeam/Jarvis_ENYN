from abc import ABC
from pathlib import Path
from typing import TYPE_CHECKING

from src import log
from src.audio import AudioOutput, AudioInput
from src.modules import Skills
from src.resources.analyze import Sentence_Analyzer
from src.services import ServiceWrapper

if TYPE_CHECKING:
    from src.core import Core


class AbstractWrapper(ABC):
    def __init__(self, core: Core):
        self.core = core
        self.messenger = self.core.messenger
        self.audio_output: AudioOutput = self.core.audio_output
        self.audio_input: AudioInput = self.core.audio_input
        self.skills: Skills = Skills()
        self.system_name: str = core.system_name
        self.path: Path = core.path
        self.local_storage: dict = core.local_storage
        self.services: ServiceWrapper = core.services
        self.analyzer: Sentence_Analyzer = core.analyzer

    def module_storage(self, module_name=None):
        module_storage = self.core.local_storage.get("module_storage")
        if module_name is None:
            return module_storage
        else:
            try:
                return module_storage[module_name]
            except IndexError:
                log.warning(f"Asked for module_storage with wrong module-name ('{module_name}')")

    def start_module(
            self, name: str = None, text: str = None, user: dict = None
    ) -> None:
        self.core.start_module(text, name, user)

    def start_module_and_confirm(
            self, name: str = None, text: str = None, user: dict = None
    ) -> bool:
        return self.core.start_module(text, name, user)
