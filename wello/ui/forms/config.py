from wtforms_alchemy import ModelForm
from wtforms.validators import ValidationError

from ... import models


class Config(ModelForm):
    class Meta:
        model = models.Config
        include = [
            'water_volume_max_delta', 'min_water_volume', 'max_water_volume',
            'tank_id',
        ]

    def validate_min_water_volume(form, field):
        if field.data >= form.max_water_volume.data:
            raise ValidationError('Cannot be higher than max volume.')

    def validate_tank_id(form, field):
        if models.tank.get(field.data) is None:
            raise ValidationError('Cannot find tank with this id.')
