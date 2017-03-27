import flask

from .. import controllers
from .. import models
from . import forms

app = flask.Flask(__name__)


@app.route('/')
def home():
    config_form = forms.Config(obj=models.config.last())
    water_volume = models.water_volume.last()

    return flask.render_template(
        'home.html',
        config_form=config_form,
        water_volume=water_volume,
    )


@app.route('/pump_in/<int:running>', methods=['POST'])
def pump_in(running):
    controllers.pump_in(running)
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
