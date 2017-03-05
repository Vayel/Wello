import flask

from .. import elec

app = flask.Flask(__name__)


@app.route('/')
def home():
    return flask.render_template('home.html')


@app.route('/switch-led', methods=['POST'])
def switch_led():
    elec.switch_led()
    return flask.redirect(flask.url_for('home'))


if __name__ == '__main__':
    app.run()
