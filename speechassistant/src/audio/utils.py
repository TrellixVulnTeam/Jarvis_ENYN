from io import BytesIO

from src.models import QueueItem, QueueType


def build_queue_item(
    queue: list[QueueItem],
    queue_type: QueueType,
    value: str | BytesIO,
    as_next: bool,
    sample_rate: int = None,
    wait_until_done: bool = False,
) -> QueueItem:
    if not sample_rate:
        sample_rate = 44100
    model: QueueItem = QueueItem(
        queue_type=queue_type,
        value=value,
        wait_until_done=wait_until_done,
        sample_rate=sample_rate,
    )
    if as_next:
        model.PRIORITY = get_highest_priority_plus_one(queue)
    return model


def get_highest_priority_plus_one(queue: list[QueueItem]) -> int:
    if len(queue) == 0:
        return 1
    return queue.__getitem__(0).PRIORITY + 1
