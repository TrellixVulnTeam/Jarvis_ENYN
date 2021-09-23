# WORK IN PROGRESS!!!!!!!!!!!!!!!!!!!!!!


from threading import Thread

import wb_server as ws


class Core:
    local_storage = None

    def __init__(self):
        with open()


if __name__ == "__maiN__":
    webThr = Thread(name=ws.Webserver, args=[core])
    webThr.daemon = True
    webThr.start()
