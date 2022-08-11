import logging

from fritzconnection import FritzConnection, FritzMonitor


class Connection:
    def __init__(self, ip="192.168.178.1"):
        self.conn = FritzConnection(address=ip)
        self.monitor = FritzMonitor(address=ip)
        logging.info(f"[INFO] Connected to FritzBox on {ip}")
        self.monitor.monitor_thread


if __name__ == "__main__":
    c = Connection()
