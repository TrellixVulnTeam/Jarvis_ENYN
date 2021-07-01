#!/usr/bin/env python3
from urllib.request import urlopen, Request
import json
import datetime
import sys
from urllib.parse import urljoin

import requests

API_URL = "https://api.corona-zahlen.org/districts/"
DISTRICT = ""


def isValid(text):
    text = text.lower().strip()
    if ('corona' in text or 'covid-19' in text) and ('info' in text or 'daten' in text or 'zahlen' in text):
        return True
    else:
        return False


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
    return {
        ags: dist for ags, dist in data.items()
        if key in dist["name"].lower()
    }


def get_info_lines(district_key):
    template = ("({ags}) {name}:\n{weekIncidence:.01f} Inzidenz, "
                "{cases} Gesamtfälle, {deaths} Verstorbene")
    result = get_district_records(district_key)
    return [template.format_map(dist) for dist in result.values()]


def handle(text, core, skill):
    district_key = core.analysis["town"] if len(sys.argv) > 1 else core.local_storage["home_location"]
    lines = get_info_lines(district_key)
    if lines:
        core.say('Ich habe folgendes herausgefunden: ' + lines)
    else:
        print("Leider habe ich den Landkreis oder die Kreisstadt nicht gefunden")