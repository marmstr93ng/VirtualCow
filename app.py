import logging
import logging.config
from flask import Flask, render_template, request, make_response, redirect
import configparser
import subprocess

logging.config.fileConfig('logging/log_settings.conf')
app = Flask(__name__)

status_file_path = "status.ini"
config = configparser.ConfigParser()

@app.route("/", methods = ["POST", "GET"])
def index():
    username = request.cookies.get('username')
    if username:
        logging.info("{} accessing the page".format(username))
    else:
        logging.info("Unknown user accessing the page")

    config.read(status_file_path)
    error = False

    version = subprocess.check_output(["git", "describe", "--always"]).strip().decode("utf-8")

    if request.method == "POST":
        if request.form["action"] == "login":
            username = request.form.get('username')
            logging.info("Logged in with {}".format(username))
            resp = make_response(redirect('/'))
            resp.set_cookie('username', username)
            return resp

        if request.form["action"] == "logout":
            logging.info("{} Logging out".format(username))
            resp = make_response(redirect('/'))
            resp.delete_cookie('username')
            return resp

        if request.form["action"] == "release":
            logging.info("Attempting to set cow free status")
            logging.info("Setting cow free status: True")
            config["Cow"]["Free"] = "True"
            config["Cow"]["Owner"] = ""
            with open(status_file_path, "w") as configfile:
                config.write(configfile)

        if request.form["action"] == "acquire":
            logging.info("Attempting to set cow free status")
            if config["Cow"]["Free"] == "False":
                logging.info("Cow already acquired by {}".format(config["Cow"]["Owner"]))
                error = True
            else:
                logging.info("Setting cow free status: False")
                config["Cow"]["Free"] = "False"
                config["Cow"]["Owner"] = username
                with open(status_file_path, "w") as configfile:
                    config.write(configfile)

    if username:
        return render_template('index.html', version=version, username=username, cow_free=config["Cow"]["Free"]== "True", cow_owner=config["Cow"]["Owner"], error=error)
    return render_template('index.html', version=version, cow_free=config["Cow"]["Free"]== "True", cow_owner=config["Cow"]["Owner"])

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
