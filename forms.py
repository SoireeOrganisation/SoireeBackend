from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired

class AddCompanyForm(FlaskForm):
    """Добавление компании"""
    name = StringField('Название', validators=[DataRequired()])
    submit = SubmitField('Добавить компанию')

class AddEmployeeForm(FlaskForm):
    """Форма добавления сотрудника"""
    surname = IntegerField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    patronomic = StringField('Отчество', validators=[DataRequired()])
    login = StringField('Логин', validators=[DataRequired()])
    companyId = SelectField('Компания', coerce=int, validators=[DataRequired()])
    roleId = SelectField('Роль', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Добавить сотрудника')