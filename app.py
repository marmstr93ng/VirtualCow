import logging
import logging.config
from flask import Flask, render_template, request
import configparser

logging.config.fileConfig('logging/log_settings.conf')
app = Flask(__name__)

status_file_path = "status.ini"
config = configparser.ConfigParser()

@app.route("/", methods = ["POST", "GET"])
def index():
    logging.info("Refreshing Index Page ...")

    config.read(status_file_path)

    if request.method == "POST":
        if request.form["action"] == "release":
            logging.info("Setting cow free status: True")
            config["Cow"]["Free"] = "True"
            with open(status_file_path, "w") as configfile:
                config.write(configfile)
        elif request.form["action"] == "acquire":
            logging.info("Setting cow free status: False")
            config["Cow"]["Free"] = "False"
            with open(status_file_path, "w") as configfile:
                config.write(configfile)

    return render_template('index.html', cow_free=config["Cow"]["Free"]== "True")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
