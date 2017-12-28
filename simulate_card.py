import flask

app = flask.Flask(__name__)

measures = {
    "pump_in": 0,
    "urban_network": 0,
    "water_distance": 0,
    "flow_in": 0,
}


@app.route("/")
def home():
    return flask.jsonify(measures)


@app.route("/pump_in", methods=['POST'])
def pump_in():
    state = flask.request.form['state']
    measures["pump_in"] = 1 if state == "1"else 0


@app.route("/urban_network", methods=['POST'])
def urban_network():
    state = flask.request.form['state']
    measures["urban_network"] = 1 if state == "1"else 0


if __name__ == "__main__":
    app.run()
