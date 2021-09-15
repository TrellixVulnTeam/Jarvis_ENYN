from phue import Bridge

if __name__ == "__main__":
    bridge = Bridge("192.168.0.191")
    bridge.connect()

    print(bridge.get_light(1))