import json

import requests

API_KEY = "d8zT1G04TG2hH5lmSTDjMciWoQt11OVD"
GEOCODE_URL = f"https://api.tomtom.com/search/2/geocode/Fullerton.json?&key={API_KEY}&query="
DISTANCE_URL = f"https://api.tomtom.com/routing/1/calculateRoute/" \
               f"33.900895,-118.083297:33.834481,-117.918290:33.870289,-117.922503" \
               f"/json?computeBestOrder=false" \
               f"&routeRepresentation=summaryOnly" \
               f"&routeType=shortest" \
               f"&avoid=unpavedRoads&key={API_KEY}"


def get_geocode(querry):
    result = requests.get(GEOCODE_URL + querry)
    json_result = result.json()
    print_result(json_result)


def print_result(json_obj):
    print(json.dumps(json_obj, indent=4))


if __name__ == "__main__":
    get_geocode(input("Querry: "))
