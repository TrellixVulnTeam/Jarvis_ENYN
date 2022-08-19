import re
import googlemaps

from src.modules import ModuleWrapper


# Python Client Library: https://github.com/googlemaps/google-maps-services-python
# Requirements: pip install -U googlemaps
# API Doc: https://developers.google.com/maps/documentation/distance-matrix/intro
# HTTP-Request: https://maps.googleapis.com/maps/api/distancematrix/json?origins=<>&destinations=<>&language=de&key=<>


def is_valid(text: str) -> bool:
    text = text.lower()
    return ("wie weit" in text or "wie lang" in text) and (
            "von" in text and ("bis" in text or "nach" in text)
    )


def handle(text: str, wrapper: ModuleWrapper) -> None:
    text = text.lower()
    length = len(text)

    gmaps = googlemaps.Client(key="AIzaSyB_zhlP1qX-Nfhgigp6C2TPpUlDfdXW_vA")

    # get locations
    matchLocations = re.search("von", text)
    if matchLocations != None:
        startLocations = matchLocations.end() + 1
        locations = text[startLocations:length]

        matchMiddle = re.search("(bis|nach)", text)
        if matchMiddle != None:
            startMiddle = matchMiddle.start() - 1
            endMiddle = matchMiddle.end() + 1

    origin = text[startLocations:startMiddle]
    destination = text[endMiddle:length]

    # get distance and duration
    directions_result = gmaps.distance_matrix(origin, destination, language="de")

    durationTxt = directions_result["rows"][0]["elements"][0]["duration"]["text"]
    distanceTxt = directions_result["rows"][0]["elements"][0]["distance"]["text"]

    match = re.search("km", distanceTxt)
    if match != None:
        endNumber = match.start() - 1
        distanceTxt = distanceTxt[0:endNumber]

        distance = float(re.sub(",", "..", distanceTxt))

    wrapper.say(
        "Von "
        + origin
        + " nach "
        + destination
        + " sind es "
        + distanceTxt
        + " Kilometer. Die Fahrt dauert "
        + durationTxt
    )


class wrapper:
    def __init__(self):
        pass

    def say(self, text):
        print(text)


if __name__ == "__main__":
    wrapper = wrapper()
    while True:
        handle(input(), wrapper, None)
