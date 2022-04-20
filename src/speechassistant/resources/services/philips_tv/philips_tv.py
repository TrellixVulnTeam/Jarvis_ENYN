import json
import os
import random
import string
import subprocess
from base64 import b64encode, b64decode

import requests
from Crypto.Hash import SHA, HMAC
from requests.auth import HTTPDigestAuth


class Pylips:
    def __init__(self):
        requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
        self.sess = requests.session()
        self.sess.verify = False
        self.sess.mount('https://', requests.adapters.HTTPAdapter(pool_connections=1))
        self.verbose = False
        # Key used for generated the HMAC signature
        self.secret_key = "JCqdN5AcnAHgJYseUn7ER5k3qgtemfUvMRghQpTfTZq7Cvv8EPQPqfz6dDxPQPSu4gKFPWkJGw32zyASgJkHwCjU"

    def run(self, host=None, user=None, password=None, body=None, command=None, verbose=None, apiv=None):
        ini_file = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "settings.ini"
        self.args = {}
        self.args["host"] = host
        self.args["user"] = user
        self.args["password"] = password
        self.args["body"] = body
        self.args["command"] = command
        self.args["verbose"] = verbose
        self.args["num_retries"] = 5
        self.args["apiv"] = apiv
        # read config file

        # check verbose option
        if self.args["verbose"] == "True":
            self.verbose = True
        else:
            self.verbose = False

        # check API version
        if self.args["apiv"] == 0:
            if self.find_api_version(self.verbose):
                if self.check_if_paired() is False:
                    print("No valid credentials found, starting pairing process...")
                    self.pair()
            else:
                if Pylips.is_online(self.args["host"]):
                    return print("IP", self.args["host"], "is online, but no known API is found. Exiting...")
                else:
                    return print("IP", self.args["host"], "seems to be offline. Exiting...")

        # load API commands
        with open(os.path.dirname(os.path.realpath(__file__)) + "/resources/tv/available_commands.json") as json_file:
            self.available_commands = json.load(json_file)

        # parse the passed self.args and run required command
        body = self.args.get('body')
        path = self.args.get('path')
        if self.args.get('command') == "get":
            self.get(path, self.verbose)
        elif self.args.get('command') == "post":
            self.post(path, body, self.verbose)
        elif len(self.args.get('command')) > 0:
            self.run_command(self.args.get('command'), body, self.verbose)
        else:
            print("Please provide a valid command with a '--command' argument")

    @staticmethod
    def is_online(host):
        """
        Returns True if host (str) responds to a ping request.
        """

        # Building the command. Ex: "ping -c 1 google.com"
        command = ["ping", "-c", "1", host]

        return subprocess.call(command) == 0

    # finds API version, saves it to settings.ini (["TV"]["apiv"]) and returns True if successful.
    def find_api_version(self, verbose=True, possible_ports=[1925], possible_api_versions=[6, 5, 1]):
        if verbose:
            print("Checking API version and port...")
        protocol = "https://"
        for port in possible_ports:
            for api_version in possible_api_versions:
                try:
                    if verbose:
                        print("Trying", str(protocol) + str(self.args["host"]) + ":" + str(port) + "/" + str(
                            api_version) + "/system")
                    r = self.sess.get(str(protocol) + str(self.args["host"]) + ":" + str(port) + "/" + str(
                        api_version) + "/system", verify=False, timeout=2)
                except requests.exceptions.ConnectionError:
                    print("Connection refused")
                    continue
                if r.status_code == 200:
                    if "api_version" in r.json():
                        self.args["apiv"] = str(r.json()["api_version"]["Major"])
                    else:
                        print("Could not find a valid API version! Pylips will try to use '", api_version, "'")
                        self.args["apiv"] = str(api_version)
                    if "featuring" in r.json() and "systemfeatures" in r.json()["featuring"] and "pairing_type" in \
                            r.json()["featuring"]["systemfeatures"] and r.json()["featuring"]["systemfeatures"][
                        "pairing_type"] == "digest_auth_pairing":
                        self.args["protocol"] = "https://"
                        self.args["port"] = "1926"
                    else:
                        self.args["protocol"] = "https://"
                        self.args["port"] = "1925"
                    return True
        return False

    # returns True if already paired or using non-Android TVs.
    def check_if_paired(self):
        if str(self.args["protocol"]) == "https://" and (
                len(str(self.args["user"])) == 0 or len(str(self.args["pass"])) == 0):
            return False
        else:
            return True

    # creates random device id
    def createDeviceId(self):
        return "".join(
            random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in
            range(16))

    # creates signature
    def create_signature(self, secret_key, to_sign):
        sign = HMAC.new(secret_key, to_sign, SHA)
        return str(b64encode(sign.hexdigest().encode()))

    # creates device spec JSON
    def getDeviceSpecJson(self, config):
        device_spec = {"device_name": "heliotrope", "device_os": "Android", "app_name": "Pylips", "type": "native"}
        device_spec["app_id"] = config["application_id"]
        device_spec["id"] = config["device_id"]
        return device_spec

    # initiates pairing with a TV
    def pair(self, err_count=0):
        payload = {}
        payload["application_id"] = "app.id"
        payload["device_id"] = self.createDeviceId()
        self.args["user"] = payload["device_id"]
        data = {"scope": ["read", "write", "control"]}
        data["device"] = self.getDeviceSpecJson(payload)
        print("Sending pairing request")
        self.pair_request(data)

    # pairs with a TV
    def pair_request(self, data, err_count=0):
        print("https://" + str(self.args["host"]) + ":1926/" + str(self.args["apiv"]) + "/pair/request")
        response = {}
        r = self.sess.post(
            "https://" + str(self.args["host"]) + ":1926/" + str(self.args["apiv"]) + "/pair/request",
            json=data, verify=False, timeout=2)
        if r.json() is not None:
            if r.json()["error_id"] == "SUCCESS":
                response = r.json()
            else:
                return print("Error", r.json())
        else:
            return print("Can not reach the API")

        auth_Timestamp = response["timestamp"]
        self.args["pass"] = response["auth_key"]
        data["device"]["auth_key"] = response["auth_key"]
        pin = input("Enter onscreen passcode: ")

        auth = {"auth_AppId": "1"}
        auth["pin"] = str(pin)
        auth["auth_timestamp"] = auth_Timestamp
        auth["auth_signature"] = self.create_signature(b64decode(self.secret_key),
                                                       str(auth_Timestamp).encode() + str(pin).encode())

        grant_request = {}
        grant_request["auth"] = auth
        data["application_id"] = "app.id"
        data["device_id"] = self.args["user"]
        grant_request["device"] = self.getDeviceSpecJson(data)

        print("Attempting to pair")
        self.pair_confirm(grant_request)

    # confirms pairing with a TV
    def pair_confirm(self, data, err_count=0):
        while err_count < 10:
            if err_count > 0:
                print("Resending pair confirm request")
            try:
                r = self.sess.post("https://" + str(self.args["host"]) + ":1926/" + str(
                    self.args["apiv"]) + "/pair/grant", json=data, verify=False,
                                   auth=HTTPDigestAuth(self.args["user"], self.args["pass"]), timeout=2)
                print("Username for subsequent calls is: " + str(self.args["user"]))
                print("Password for subsequent calls is: " + str(self.args["pass"]))
                return print("The credentials are saved in the settings.ini file.")
            except Exception:
                # try again
                err_count += 1
                continue
        else:
            return print("The API is unreachable. Try restarting your TV and pairing again")

    # sends a general GET request
    def get(self, path, verbose=True, err_count=0, print_response=True):
        while err_count < int(self.args["num_retries"]):
            if verbose:
                print("Sending GET request to",
                      str(self.args["protocol"]) + str(self.args["host"]) + ":" + str(
                          self.args["port"]) + "/" + str(self.args["apiv"]) + "/" + str(path))
            try:
                r = self.sess.get(str(self.args["protocol"]) + str(self.args["host"]) + ":" + str(
                    self.args["port"]) + "/" + str(self.args["apiv"]) + "/" + str(path), verify=False,
                                  auth=HTTPDigestAuth(str(self.args["user"]), str(self.args["pass"])),
                                  timeout=2)
            except Exception:
                err_count += 1
                continue
            if verbose:
                print("Request sent!")
            if len(r.text) > 0:
                if print_response:
                    print(r.text)
                return r.text

    # sends a general POST request
    def post(self, path, body, verbose=True, callback=True, err_count=0):
        if type(body) is str:
            body = json.loads(body)
        if verbose:
            print("Sending POST request to",
                  'https://' + self.args['host'] + ":" + '1926' + "/" + str(6) + "/" + str(path))
        try:
            r = self.sess.post('https://' + self.args['host'] + ":" + '1926' + "/" + str(6) + "/" + str(path),
                               json=body,
                               verify=False,
                               auth=HTTPDigestAuth(str(self.args["user"]), str(self.args["password"])),
                               timeout=2)
        except Exception:
            err_count += 1
        if verbose:
            print("Request sent!")
        if len(r.text) > 0:
            print(r.text)
            return r.text
        elif r.status_code == 200:
            print(json.dumps({"response": "OK"}))
            return json.dumps({"response": "OK"})

    # runs a command
    def run_command(self, command, body=None, verbose=True, callback=True, print_response=True):
        if command in self.available_commands["get"]:
            return self.get(self.available_commands["get"][command]["path"], verbose, 0, print_response)
        elif command in self.available_commands["post"]:
            if "body" in self.available_commands["post"][command] and body is None:
                if "input_" in command:
                    body = self.available_commands["post"]["google_assistant"]["body"]
                    path = self.available_commands["post"]["google_assistant"]["path"]
                    body["intent"]["extras"]["query"] = self.available_commands["post"][command]["body"]["query"]
                else:
                    body = self.available_commands["post"][command]["body"]
                    path = self.available_commands["post"][command]["path"]
                return self.post(path, body, verbose, callback)
            if "body" in self.available_commands["post"][command] and body is not None:
                if type(body) is str:
                    body = json.loads(body)
                new_body = self.available_commands["post"][command]["body"]
                if command == "ambilight_brightness":
                    new_body["values"][0]["value"]["data"] = body
                elif command == "ambilight_color":
                    new_body["colorSettings"]["color"]["hue"] = int(body["hue"] * (255 / 360))
                    new_body["colorSettings"]["color"]["saturation"] = int(body["saturation"] * (255 / 100))
                    new_body["colorSettings"]["color"]["brightness"] = int(body["brightness"])
                elif command == "google_assistant":
                    new_body["intent"]["extras"]["query"] = body["query"]
                elif "input_" in command:
                    new_body = self.available_commands["google_assistant"][command]
                    new_body["intent"]["extras"]["query"] = self.available_commands["post"][command]["body"]["query"]
                return self.post(self.available_commands["post"][command]["path"], new_body, verbose, callback)
            else:
                return self.post(self.available_commands["post"][command]["path"], body, verbose, callback)
        elif command in self.available_commands["power"]:
            return self.sess.post(
                "https://" + str(self.args["host"]) + ":8008/" + self.available_commands["power"][command][
                    "path"], verify=False, timeout=2)
        else:
            print("Unknown command")

