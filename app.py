import logging
import logging.config
from flask import Flask, render_template, request, make_response, redirect
import configparser

logging.config.fileConfig('logging/log_settings.conf')
app = Flask(__name__)

status_file_path = "status.ini"
config = configparser.ConfigParser()

@app.route("/", methods = ["POST", "GET"])
def index():
    logging.info("Refreshing Index Page ...")

    username = request.cookies.get('username')
    config.read(status_file_path)

    if request.method == "POST":
        if request.form["action"] == "login":
            username = request.form.get('username')
            logging.info("Logged in with {}".format(username))
            resp = make_response(redirect('/'))
            resp.set_cookie('username', username)
            return resp

        if request.form["action"] == "logout":
            resp = make_response(redirect('/'))
            resp.delete_cookie('username')
            return resp

        if request.form["action"] == "release":
            logging.info("Setting cow free status: True")
            config["Cow"]["Free"] = "True"
            with open(status_file_path, "w") as configfile:
                config.write(configfile)

        if request.form["action"] == "acquire":
            logging.info("Setting cow free status: False")
            config["Cow"]["Free"] = "False"
            with open(status_file_path, "w") as configfile:
                config.write(configfile)

    if username:
        return render_template('index.html', username=username, cow_free=config["Cow"]["Free"]== "True")
    return render_template('index.html', cow_free=config["Cow"]["Free"]== "True")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
