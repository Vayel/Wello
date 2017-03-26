import flask

from .. import controllers

app = flask.Flask(__name__)


@app.route('/')
def home():
    return flask.render_template('home.html')


@app.route('/pump_in/<int:running>', methods=['POST'])
def pump_in(running):
    controllers.pump_in(running)
    return flask.redirect(flask.url_for('home'))


if __name__ == '__main__':
    app.run()
