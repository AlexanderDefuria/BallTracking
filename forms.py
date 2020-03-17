from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Length


class HSVForm(FlaskForm):
    high_H = IntegerField('H upper', default=None)
    high_S = IntegerField('S upper', default=None)
    high_V = IntegerField('V upper', default=None)

    low_H = IntegerField('H low', default=None)
    low_S = IntegerField('S low', default=None)
    low_V = IntegerField('V low', default=None)


