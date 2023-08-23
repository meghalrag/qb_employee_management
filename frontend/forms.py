import re
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField
from wtforms.validators import ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from validator import is_valid_email_phone_field


designation_choices = [
    ('Software Engineer', 'Software Engineer'), 
    ('Senior Engineer', 'Senior Engineer'), 
    ('Lead Engineer', 'Lead Engineer'), 
    ('QA Engineer', 'QA Engineer'), 
    ('Associate Architect', 'Associate Architect')
]

department_choices = [
    ('Python', 'Python'),
    ('Java', 'Java'),
    ('PHP', 'PHP'),
    ('DevOps', 'DevOps'),
]

manager_choices = [
    ('0', "No Manager"),
    ('meghalrag@123.com', "meghalrag@123.com")
]

class SignupForm(FlaskForm):
    """User Sign-up Form."""

    name = StringField("Name", validators=[DataRequired()], render_kw={'class': 'form-control'})
    email = StringField(
        "Email",
        validators=[
            Length(min=6),
            Email(message="Enter a valid email."),
            DataRequired(),
        ],
        render_kw={'class': 'form-control'}
    )
    phone_number = StringField("Phone Number", validators=[DataRequired()], render_kw={'class': 'form-control'})
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, message="Select a stronger password."),
        ],
        render_kw={'class': 'form-control'}
    )
    confirm = PasswordField(
        "Confirm Your Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
        render_kw={'class': 'form-control'}
    )
    designation = SelectField('Select an option', choices=designation_choices, validators=[DataRequired()], render_kw={'class': 'form-control'})
    department = SelectField('Select an option', choices=department_choices, validators=[DataRequired()], render_kw={'class': 'form-control'})
    manager = SelectField('Select an option', choices=manager_choices, validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField("Create", render_kw={'class': 'btn btn-success'})

    def validate_phone_number(form, field):
        if is_valid_email_phone_field(field.data):
             pass
        else:
             raise ValidationError("Invalid Phone Number")
        
    def validate_name(form, field):
        if field.data.replace(" ", "").isalpha():
            pass
        else:
            raise ValidationError("Enter a valid Name")
        

class EmployeeEditForm(FlaskForm):
    """User Sign-up Form."""

    name = StringField("Name", validators=[DataRequired()], render_kw={'class': 'form-control'})
    email = StringField(
        "Email",
        validators=[
            Length(min=6),
            Email(message="Enter a valid email."),
            DataRequired(),
        ],
        render_kw={'class': 'form-control', 'readonly': True}
    )
    phone_number = StringField("Phone Number", validators=[DataRequired()], render_kw={'class': 'form-control', 'readonly': True})
    designation = SelectField('Select an option', choices=designation_choices, validators=[DataRequired()], render_kw={'class': 'form-control'})
    department = SelectField('Select an option', choices=department_choices, validators=[DataRequired()], render_kw={'class': 'form-control'})
    manager = SelectField('Select an option', choices=manager_choices, validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField("Update", render_kw={'class': 'btn btn-success'})

    def validate_phone_number(form, field):
        if is_valid_email_phone_field(field.data):
            pass
        else:
            raise ValidationError("Invalid Phone Number")
        
    def validate_name(form, field):
        if field.data.replace(" ", "").isalpha():
            pass
        else:
            raise ValidationError("Enter a valid Name")
              


class LoginForm(FlaskForm):
    """User Log-in Form."""

    email_or_phone = StringField(
        "Email/Phone Number", validators=[DataRequired()], 
        render_kw={'class': 'form-control'}
    )
    password = PasswordField("Password", validators=[DataRequired()], render_kw={'class': 'form-control'})
    submit = SubmitField("Login", render_kw={'class': 'btn btn-success'})

    def validate_email_or_phone(form, field):
        if is_valid_email_phone_field(field.data):
             pass
        else:
             raise ValidationError("Invalid Email or Phone Number")

    