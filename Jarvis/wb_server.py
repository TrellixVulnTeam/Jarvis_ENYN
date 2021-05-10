#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import base64
import logging
import shutil

from flask import Flask, render_template, jsonify, request, send_file, make_response, redirect
from gevent import pywsgi
from Crypto import Random
import json
import os
import sys
from webserver.helpWrapper import InstallWrapper

# JARVIS_setup_wrapper-import is a bit hacky but I can't see any nicer way to realize it yet
sys.path.append(os.path.join(os.path.dirname(__file__), "/"))
from distutils.dir_util import copy_tree


def Webserver(core):
    webapp = Flask("JARVIS", template_folder="webserver/template", static_folder="webserver/static")
    installer = InstallWrapper()

    def getData():
        data = request.args.to_dict()
        data.update(request.form.to_dict())
        return data

    # ------------------------------------------------------------------------------
    # HTTP-Frontend
    # ------------------------------------------------------------------------------

    nav = [
    {"href": "/setup", "text": "\"Erste Schritte\""},
    {"href": "/setupSystem", "text": "Server einrichten"},
    {"href": "/setupUser", "text": "Benutzer erstellen"},
    {"href": "/setupModules", "text": "Module bearbeiten (WIP)"},
    ]


    @webapp.route("/")
    @webapp.route("/index")
    def index():
        firstTime = False
        if firstTime:
            return redirect("/setup")
        else:
            return render_template("index.html", nav=nav)

    @webapp.route("/setup")
    def setup_1():
        return render_template("setup.html", nav=nav)

    @webapp.route("/setup_2")
    def setup_2():
        firstData = installer.listPackages()
        return render_template("setup_checkServices.html", nav=nav, fD=firstData)

    @webapp.route("/setup_3")
    def setup_3():
        return render_template("setup_menu.html", nav=nav)

    @webapp.route("/setupSystem")
    def setupSystem():
        data = getData()
        if os.path.exists("config.json"):
            g = True    # "config-exists"-trigger
        else:
            g = False
        with open("config.json") as conf:
            config = json.load(conf)
        standards = {
            "name": config["System_name"],
            "homeLocation": config["Local_storage"]["home_location"],
            "generateKey": True if config["Network_Key"] == "" else False,
            "useCameras": True if config["use_cameras"] else False,
            "useFaceRec": True if config["use_facerec"] else False,
            "useInterface": True if config["use_interface"] else False,
        }
        return render_template("setupSystem.html", nav=nav, st=standards, gold=g)

    @webapp.route("/setupUser")     # TODO
    def setupUser():
        data = getData()
        gold = os.path.exists("temp_files/user_temp")
        gold = gold and os.path.exists("users/")
        gold = gold and os.path.exists("config.json")
        # per default a set of normal standard-values is loaded, via javascript and
        # the API-Endpoint "/api/loadConfig/user/<username>" another config-file can
        # be edited with that /setupUser-File.
        with open("temp_files/user_temp/data.json", "r") as confFile:
            config = json.load(confFile)
        with open("config.json", "r") as confFile:
            ServerConfig = json.load(confFile)
        standards = {
            "userName": "",
            "userRole": config["User_Info"]["role"],
            "userTelegram": config["User_Info"]["telegram_id"] if "telegram" in ServerConfig and "telegram_id" in config["User_Info"] else "-1",
            "userFullName": config["User_Info"]["first_name"],
            "userFullLastName": config["User_Info"]["last_name"],
            "userBirthYear": config["User_Info"]["date_of_birth"]["year"],
            "userBirthMonth": config["User_Info"]["date_of_birth"]["month"],
            "userBirthDay": config["User_Info"]["date_of_birth"]["day"]
        }
        return render_template("setupUser.html", nav=nav, st=standards, gold=gold)

    # API-like-Calls

    @webapp.route("/api/installer/listPackages")
    @webapp.route("/api/installer/listPackages/<extended>")
    def listPackages(extended=False):
        if extended == "details":
            extended = True
        else:
            extended = False
        data = installer.listPackages(extended)
        return jsonify(data)

    @webapp.route("/api/installer/getStatus")
    def getStatus():
        data = installer.getInstallerStatus()
        return jsonify(data)

    @webapp.route("/api/installer/startInstallation/<packageName>")
    def startInstallation(packageName):
        data = installer.startInstallation(packageName)
        return jsonify(data)

    @webapp.route("/api/setup/prerequesites") # TODO
    def getPrereqSetup():
        """
        checks things which would be checked on setup start
        os.path.exists('config.json') for example
        """
        data = {}
        return jsonify(data)

    @webapp.route("/api/writeConfig/system")
    def writeSystemConfig():
        print("start")
        data = getData()
        with open("config.json", "r") as config_file:
            config_data = json.load(config_file)
        # check every parameter and update those in the config file
        if "System_name" in data and data["System_name"].strip() != "":
            config_data["System_name"] = data["JARVISName"]

        if "voice" in data and data["voice"].strip() != "":
            config_data["voice"] = data["voice"]

        if "homeLocation" in data and data["homeLocation"].strip() != "":
            config_data['Local_storage']['home_location'] = data['homeLocation']

        if "messengerKey" in data and len(data["messengerKey"].strip()) == 45:
            config_data["messenger_key"] = data["messengerKey"].strip()
            config_data["messenger"] = True

        if "useCameras" in data and data["useCameras"].strip() != "":
            t = True if data["useCameras"] == "true" else False
            config_data["use_cameras"] = t
            bedingt_kopieren('./resources/optional_modules/recieve_cameras.py', './modules/continuous/recieve_cameras.py', t)

            if "useFaceRec" in data and data["useFaceRec"].strip() != "":
                t = True if data["useFaceRec"] == "true" else False
                config_data["use_facerec"] = t
                bedingt_kopieren('./resources/optional_modules/face_recognition.py', './modules/continuous/face_recognition.py', t)
                bedingt_kopieren('./resources/optional_modules/retrain_facerec.py', './modules/retrain_facerec.py', t)

            if "useInterface" in data and data["useInterface"].strip() != "":
                t = True if data["useInterface"] == "true" else False
                config_data["use_interface"] = t
                bedingt_kopieren('./resources/optional_modules/POI_Interface.py', './modules/continuous/POI_Interface.py', t)
                bedingt_kopieren('./resources/optional_modules/POI_Interface_controls.py', './modules/POI_Interface_controls.py', t)
        if config_data["Network_Key"] == "":
            config_data["Network_Key"] = generate_key(32)
        with open('config.json', 'w') as config_file:
            json.dump(config_data, config_file, indent=4)
            return "ok"
        return "err"

    @webapp.route("/api/writeConfig/user/<userName>")   # TODO
    def writeUserConfig(userName):
        data = getData()
        if "userName" in data and data["userName"].strip() != "":
            filename = "./users/" + data["userName"] + "/data.json"
            default_path = "temp_files/user_temp/data.json"
            if os.path.exists(filename):
                with open(filename, "r") as config_file:
                    config_data = json.load(config_file)
            elif os.path.exists(default_path):
                with open(default_path, "r") as config_file:
                    config_data = json.load(config_file)
            else:
                config_data = {"User_Info": {}}
            config_data["User_Info"]["name"] = data["userName"]

            subdirs = os.listdir("users")
            config_data["User_Info"]["uid"] = len(subdirs) + 1

            if "userRole" in data and data["userRole"].strip() != "":
                if data["userRole"].strip() in ["USER", "ADMIN"]:
                    config_data["User_Info"]["role"] = data["userRole"]

            if "userTelegram" in data and data["userTelegram"].strip() != "":
                try:
                    config_data["User_Info"]["telegram_id"] = int(data["userTelegram"])
                except ValueError:
                    config_data["User_Info"]["telegram_id"] = 0

            if "userFullName" in data and data["userFullName"].strip() != "":
                config_data["User_Info"]["first_name"] = data["userFullName"]
            if "userFullLastName" in data and data["userFullLastName"].strip() != "":
                config_data["User_Info"]["last_name"] = data["userFullLastName"]

            if "userBirthYear" in data and data["userBirthYear"].strip() != "":
                try:
                    config_data["User_Info"]["date_of_birth"]["year"] = int(data["userBirthYear"])
                except ValueError:
                    config_data["User_Info"]["date_of_birth"]["year"] = 0

            if "userBirthMonth" in data and data["userBirthMonth"].strip() != "":
                try:
                    config_data["User_Info"]["date_of_birth"]["month"] = int(data["userBirthMonth"])
                except ValueError:
                    config_data["User_Info"]["date_of_birth"]["month"] = 0

            if "userBirthDay" in data and data["userBirthDay"].strip() != "":
                try:
                    config_data["User_Info"]["date_of_birth"]["day"] = int(data["userBirthDay"])
                except ValueError:
                    config_data["User_Info"]["date_of_birth"]["day"] = 0

            if not os.path.exists("./users" + config_data["User_Info"]["name"]):
                try:
                    os.mkdir("./users/" + config_data["User_Info"]["name"])
                except FileExistsError:
                    pass
            try:
                copy_tree("temp_files/user_temp", "./users/" + config_data["User_Info"]["name"])
            except IOError:
                print('\n' '[ERROR] Fehler beim kopieren der Dateien. Bitte versuche, den Setup-Assistent mit Root-Rechten auszuführen.')
                return "err"
            with open('./users/' + config_data['User_Info']['name'] + '/data.json', 'w') as config_file:
                json.dump(config_data, config_file, indent=4)
            # update Userlist
            core.users.load_users()
            return "ok"
        else:
            return "err"


    @webapp.route("/api/loadConfig/user/<userName>")
    def loadUserConfig(userName):
        if os.path.exists("./users/" + userName + "/data.json"):
            with open("./users/" + userName + "/data.json", "r") as confFile:
                config = json.load(confFile)["User_Info"]
            data = {
                "userName": config["name"],
                "userRole": config["role"],
                "userID": config["uid"],
                "userTelegram": config["messenger_id"],
                "userBirthYear": config["date_of_birth"]["year"],
                "userBirthMonth": config["date_of_birth"]["month"],
                "userBirthDay": config["date_of_birth"]["day"],
                "userFullName": config["first_name"],
                "userFullLastName": config["last_name"],
                "alarmSound": config["wecker_ton"],
                "waitingMessages": config["wartende_benachrichtigungen"]
            }
            return jsonify(data)
        else:
            return jsonify("user not found")

    @webapp.route("/api/server/<action>") # TODO
    def getServerStatus(action):
        if action == "stopp":
            return 'ok'
        else:
            data = "err"
        return jsonify(data)

    @webapp.route("/api/server/list/<action>")
    def getExtraServerStatus(action="*"):
        feed = core.local_storage
        users = core.users.get_user_list()
        modules = core.local_storage["modules"]

        externSystems = {
                "Phillips HUE": {
                    "name": "Phillips Hue",
                    "established": True if feed["module_storage"]["phillips_hue"]["Bridge-IP"] != "" else False
                },
                "Phillips TV": {
                    "name": "Phillips TV",
                    "established": True if (feed["module_storage"]["phillips-tv"]["user"] != ""
                                            and feed["module_storage"]["phillips-tv"]["pass"] != ""
                                            and feed["module_storage"]["phillips-tv"]["host"] != "") else False
                }
        }

        if action == "users":
            data = feed["users"] if "users" in feed else {}
        elif action == "modules":
            data = feed["modules"] if "modules" in feed else {}
        elif action == "telegram":
            data = feed["rejected_telegram_messages"] if "rejected_telegram_messages" in feed else []
        elif action == "externSystems":
            data = externSystems
        else:
            data = {
                "users": users,
                "modules": modules,
                "telegram": True if feed["messenger_allowed_id_table"] != [] else [],
                "externSystems": externSystems
            }
        return jsonify(data)

    @webapp.route("/api/module/list")
    def listModules():
        feed = core.local_storage
        return jsonify(feed["modules"] if "modules" in feed else {})

    @webapp.route("/api/module/<modName>/<action>")     # TODO
    def changeModuleMode(modName, action):
        modules = [] # dummyList
        if modName in modules:
            if action == "load":
                pass
            elif action == "unload":
                pass
            elif action == "status":
                pass
        return "ok"

    @webapp.errorhandler(404)
    def error_404(error):
        return render_template('404.html'), 404

    @webapp.errorhandler(500)
    def error_500(error):
        return render_template('500.html'), 500

    def bedingt_kopieren(ursprung, ziel, copy):
        if copy:
            if os.path.exists(ziel):
                return
            else:
                shutil.copy(ursprung, ziel)
        else:
            if os.path.exists(ziel):
                os.remove(ziel)

    def generate_key(length):
        key = Random.get_random_bytes(length)
        key_encoded = base64.b64encode(key)
        key_string = key_encoded.decode('utf-8')
        return key_string

    ws = pywsgi.WSGIServer(("0.0.0.0", 50500), webapp)
    print("To connect to the JARVIS-Webserver, please visit http://localhost:50500/setup ")
    ws.serve_forever()
