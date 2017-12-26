import requests
from wtforms_alchemy import ModelForm
from wtforms.validators import ValidationError

from ... import models


class Config(ModelForm):
    class Meta:
        model = models.Config
        include = [
            'water_volume_max_delta', 'min_water_volume', 'max_water_volume',
            'tank_id', 'card_ip',
        ]

    def validate_card_ip(form, field):
        url = "http://" + field.data
        try:
            requests.get(url)
        except requests.exceptions.MissingSchema:
            raise ValidationError('Invalid ip.')
        except requests.exceptions.ConnectionError:
            raise ValidationError('Cannot connect to this host.')

    def validate_min_water_volume(form, field):
        if field.data >= form.max_water_volume.data:
            raise ValidationError('Cannot be higher than max volume.')

    def validate_max_water_volume(form, field):
        try:
            Config.validate_tank_id(form, form.tank_id)
        except ValidationError:
            return

        tank = models.tank.get(form.tank_id.data)
        if field.data > tank.volume:
            raise ValidationError(
                'Must be lower than the volume of the tank ({0}).'.format(tank.volume)
            )

    def validate_tank_id(form, field):
        if models.tank.get(field.data) is None:
            raise ValidationError('Cannot find tank with this id.')
