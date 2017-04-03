from wtforms_alchemy import ModelForm

from ... import models


class CylinderTank(ModelForm):
    class Meta:
        model = models.CylinderTank
