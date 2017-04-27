from wtforms_alchemy import ModelForm

from ... import models


class CuboidTank(ModelForm):
    class Meta:
        model = models.CuboidTank
