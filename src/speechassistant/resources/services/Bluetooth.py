import bluetooth

if __name__ == "__main__":
    devices = bluetooth.discover_devices(lookup_names=True, lookup_class=True)

    number_of_devices = len(devices)
    print(f"{number_of_devices} devices found")
    for addr, name, device_class in devices:
        print("\n Device:")
        print(f"Device Name: {name}")
        print(f"Device Mac Address: {addr}")
        print(f"Device Class: {device_class}\n")
