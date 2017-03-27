from wtforms_alchemy import ModelForm

from ... import models


class Config(ModelForm):
    class Meta:
        model = models.Config
