import logging
import struct
from datetime import datetime

import pvporcupine
import pyaudio


if __name__ == "__main__":

    access_key = "1mQJEO2ad9yDRxrOi8M7N5e0c/wnHm8WHyGFhTn5VwsYzsiimoBZaQ=="
    porcupine = pvporcupine.create(access_key=access_key, keywords=["jarvis"])

    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length,
    )

    logging.info("\nListening {%s}" % {"jarvis"})

    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            logging.info(
                f"[ACTION] Detected JARVIS at "
                f"{datetime.now().hour}:{datetime.now().minute}"
            )
