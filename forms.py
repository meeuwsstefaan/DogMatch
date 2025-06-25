# Python
import datetime as dt

from flask_wtf import FlaskForm
from wtforms import (
    StringField, SelectField,
    TimeField, SubmitField
)
from wtforms.validators import DataRequired

from models import DogOwner

WEEKDAYS = [(i, day) for i, day in enumerate(
    ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
)]


class OwnerForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("E-mail")
    submit = SubmitField("Save")


class DogForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    breed = StringField("Breed")
    owner_id = SelectField("Owner", coerce=int)

    submit = SubmitField("Save")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner_id.choices = [
            (o.id, o.name) for o in DogOwner.query.order_by(DogOwner.name).all()
        ]


class WalkerForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    phone = StringField("Phone")
    submit = SubmitField("Save")


class AvailabilityForm(FlaskForm):
    weekday = SelectField("Weekday", coerce=int, choices=WEEKDAYS)
    start_time = TimeField("Start", default=dt.time(9, 0))
    end_time   = TimeField("End",   default=dt.time(17, 0))
    submit = SubmitField("Add")

    # WTForms 3.x passes 'extra_validators', so we must accept it.
    def validate(self, extra_validators=None):
        rv = super().validate(extra_validators=extra_validators)
        if not rv:
            return False
        if self.start_time.data >= self.end_time.data:
            self.start_time.errors.append("Start must be before End")
            return False
        return True
