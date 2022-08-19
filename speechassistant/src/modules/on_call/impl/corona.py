#!/usr/bin/env python3
import sys
from urllib.parse import urljoin

import requests

from src.modules import ModuleWrapper

API_URL = "https://api.corona-zahlen.org/districts/"
DISTRICT = ""


# toDO: refactor

def isValid(text: str) -> bool:
    text = text.lower().strip()
    return ("corona" in text or "covid-19" in text) and (
            "info" in text or "daten" in text or "zahlen" in text
    )


def get_json(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_district_records(district_key):
    key = str(district_key).lower()
    if key.isdigit():
        district_url = urljoin(API_URL, key)
        return get_json(district_url)["data"]
    data = get_json(API_URL)["data"]
    return {ags: dist for ags, dist in data.items() if key in dist["name"].lower()}


def get_info_lines(district_key):
    template = (
        "({ags}) {name}:\n{weekIncidence:.01f} Inzidenz, "
        "{cases} Gesamtfälle, {deaths} Verstorbene"
    )
    result = get_district_records(district_key)
    return [template.format_map(dist) for dist in result.values()]


def handle(text: str, wrapper: ModuleWrapper) -> None:
    district_key = (
        wrapper.analysis["town"]
        if len(sys.argv) > 1
        else wrapper.local_storage["home_location"]
    )
    lines = get_info_lines(district_key)
    if lines:
        wrapper.say("Ich habe folgendes herausgefunden: " + lines)
    else:
        print("Leider habe ich den Landkreis oder die Kreisstadt nicht gefunden")
