class TimeObserver:
    def __int__(self, duration_in_seconds: int):
        self.observer: Obser
        self.duration_in_seconds = duration_in_seconds
        self.subscriber_counter = 0

    def run(self) -> None:
        pass
