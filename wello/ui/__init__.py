import flask

from .. import elec

app = flask.Flask(__name__)
app.DEBUG = True

led_on = False


@app.route('/')
def home():
    return flask.render_template('home.html')


@app.route('/switch-led', methods=['POST'])
def switch_led():
    global led_on
    elec.cmd_led(led_on)
    led_on = not led_on
    return flask.redirect(flask.url_for('home'))


if __name__ == '__main__':
    app.run()
