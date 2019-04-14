import logging
import logging.config
from flask import Flask, render_template

logging.config.fileConfig('logging/log_settings.conf')
app = Flask(__name__)

@app.route("/")
def index():
    logging.info("Refreshing Index Page ...")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
