from flask_wtf import Form
from wtforms import TextField, IntegerField
from wtforms.validators import DataRequired, Length


class add_student(Form):
    student_name = TextField(
        'Student Name', validators=[DataRequired(), Length(min=6, max=25)]
    )

    academics = IntegerField(
        'Academics Score', validators=[DataRequired(), Length(min=2, max=25)]
    )

    sports = IntegerField(
        'Sports Score', validators=[DataRequired(), Length(min=2, max=25)]
    )

    social = IntegerField(
        'Social Score', validators=[DataRequired(), Length(min=2, max=25)]
    )


class Update_student_info(Form):
    academics = IntegerField(
        'Academics Score', validators=[DataRequired(), Length(min=2, max=25)]
    )

    sports = IntegerField(
        'Sports Score', validators=[DataRequired(), Length(min=2, max=25)]
    )

    social = IntegerField(
        'Social Score', validators=[DataRequired(), Length(min=2, max=25)]
    )
