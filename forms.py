from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField
from functools import wraps
from flask import redirect, url_for, abort
from flask_login import current_user


class UploadProject(FlaskForm):
    title = StringField('Project Name: ', validators=[DataRequired()])
    subtitle = StringField('Subtle Description: ', validators=[DataRequired()])
    img_url = StringField('Project Preview', validators=[DataRequired(), URL()])
    body = CKEditorField(label='Project Description', validators=[DataRequired()])
    techniques_applied = StringField('Concepts Applied', validators=[DataRequired()])
    upload = SubmitField('Upload Project')

