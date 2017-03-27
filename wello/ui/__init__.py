import flask

from .. import controllers, exceptions, models
from . import forms

app = flask.Flask(__name__)

try:
    app.config.from_pyfile('flask.cfg')
except FileNotFoundError:
    pass

try:
    app.config.from_envvar('WELLO_FLASK_CONFIG_FILE')
except RuntimeError:
    pass


@app.route('/')
def home():
    config_form = forms.Config(obj=models.config.last())
    water_volume = models.water_volume.last()
    pump_in_command = models.pump_in_command.last()

    return flask.render_template(
        'home.html',
        config_form=config_form,
        water_volume=water_volume,
        pump_in=pump_in_command,
    )


@app.route('/pump_in/<int:running>', methods=['POST'])
def pump_in(running):
    try:
        controllers.pump_in(running)
    except exceptions.TankMayOverflow:
        flask.flash('Allumer la pompe peut faire déborder la cuve.', 'error')

    return flask.redirect(flask.url_for('home'))


@app.route('/configure', methods=['POST'])
def configure():
    form = forms.Config(flask.request.form)

    if form.validate():
        config = models.Config()
        form.populate_obj(config)

        models.save(config)

    return flask.redirect(flask.url_for('home'))


if __name__ == '__main__':
    app.run()
