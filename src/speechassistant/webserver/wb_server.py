#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import mimetypes

from flask import Flask, render_template, jsonify, request, Response, send_file


def Webserver(_core, _temp_module_wrapper):
    app: Flask = Flask("JARVIS")

    app.config["JSON_SORT_KEYS"] = False

    def getData():
        data = request.args.to_dict()
        data.update(request.form.to_dict())
        return data

    @app.route("/api/v1", methods=["GET"])
    def index():
        return {}

    @app.route("/api/v1/sounds", methods=["GET", "POST"])
    def upload_alarm_sound():
        pass

    @app.route("/api/v1/hotword/<action>", methods=["GET", "POST"])
    def hotword_informations():
        pass

    @app.route("/api/v1/weather", methods=["GET"])
    def weather():
        pass

    @app.route("/api/v1/apiconfig", methods=["GET", "POST"])
    def api_keys():
        pass

    @app.route("/api/v1/routine", methods=["GET", "POST"])
    @app.route("/api/v1/routine/<rid>", methods=["GET", "POST"])
    def routines(rid: int):
        if rid is None and request.args.get("id") is None:
            return "No ID was given!", 400

    @app.route("/api/v1/services/<name>", methods=["GET"])
    def services(name: str):
        if name is None and request.args.get("name") is None:
            return "No name was given!", 400

    @app.route("/api/v1/timer", methods=["GET", "POST", "UPDATE", "DELETE"])
    @app.route("/api/v1/timer/<tid>", methods=["GET", "POST", "UPDATE", "DELETE"])
    def timer(tid: int):
        if tid is None and request.args.get("id") is None:
            return "No ID was given!", 400

    @app.route("/api/v1/alarm", methods=["GET", "POST", "UPDATE", "DELETE"])
    @app.route("/api/v1/alarm/<aid>", methods=["GET", "POST", "UPDATE", "DELETE"])
    def alarm(aid: int):
        if aid is None and request.args.get("id") is None:
            return "No ID was given!", 400

        if request.method == "GET":
            pass
        elif request.method == "POST":
            pass
        elif request.method == "UPDATE":
            pass
        elif request.method == "DELETE":
            pass

    @app.route("/api/v1/lights", methods=["GET"])
    def get_lights():
        pass


"""
        if request.method == 'GET':
            pass
        elif request.method == 'POST':
            pass
        elif request.method == 'UPDATE':
            pass
        elif request.method == 'DELETE':
            pass
"""
