from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    description = StringField("description", validators=[DataRequired()])
    due_day = DateField("due_day", format='%Y-%m-%d')
    important = BooleanField("important")
    submit = SubmitField('Add Task')


class EditForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    description = StringField("description", validators=[DataRequired()])
    due_day = DateField("due_day", format='%Y-%m-%d')
    important = BooleanField("important")
    submit = SubmitField('Edit Task')


class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')