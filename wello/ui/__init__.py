from functools import wraps

import flask
import flask_socketio

from .. import controllers, exceptions, models
from . import forms

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

try:
    app.config.from_pyfile('flask.cfg')
except FileNotFoundError:
    pass

try:
    app.config.from_envvar('WELLO_FLASK_CONFIG_FILE')
except RuntimeError:
    pass


def need_config(func):
    @wraps(func)  # For Flask
    def wrapper(*args, **kwargs):
        if not models.config.is_valid():
            flask.flash("L'application nécessite d'être configurée.", 'error')
            return flask.redirect(flask.url_for('config'))

        return func(*args, **kwargs)
    return wrapper


@app.route('/')
@need_config
def home():
    water_volume = models.water_volume.last()
    pump_in = models.pump_in_state.last()

    return flask.render_template(
        'home.html',
        water_volume=water_volume,
        pump_in=pump_in,
    )


@app.route('/pump_in/<int:running>', methods=['POST'])
@need_config
def pump_in(running):
    try:
        controllers.pump_in(running)
    except exceptions.TankMayOverflow:
        flask.flash('Allumer la pompe peut faire déborder la cuve.', 'error')

    return flask.redirect(flask.url_for('home'))


@app.route('/config', methods=['GET', 'POST'])
def config():
    if flask.request.method == 'POST':
        form = forms.Config(flask.request.form)

        if form.validate():
            config = models.Config()
            form.populate_obj(config)

            models.save(config)

            flask.flash("Configuration réussie.", 'success')
            return flask.redirect(flask.url_for('home'))
    else:
        form = forms.Config(obj=models.config.last())

    return flask.render_template('config.html', form=form)


@app.route('/create-cylinder-tank', methods=['GET', 'POST'])
def create_cylinder_tank():
    if flask.request.method == 'POST':
        form = forms.CylinderTank(flask.request.form)

        if form.validate():
            model = models.CylinderTank()
            form.populate_obj(model)

            models.save(model)

            return flask.redirect(flask.url_for('config'))
    else:
        form = forms.CylinderTank()

    return flask.render_template('create_cylinder_tank.html', form=form)


@app.route('/create-cuboid-tank', methods=['GET', 'POST'])
def create_cuboid_tank():
    if flask.request.method == 'POST':
        form = forms.CuboidTank(flask.request.form)

        if form.validate():
            model = models.CuboidTank()
            form.populate_obj(model)

            models.save(model)

            return flask.redirect(flask.url_for('config'))
    else:
        form = forms.CuboidTank()

    return flask.render_template('create_cuboid_tank.html', form=form)


def update_pump_in_state(running, **kwargs):
    socketio.emit('pump_in_state', {'running': running})
