from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import PasswordField, SelectField
from wtforms.validators import DataRequired


class UserModelView(ModelView):
    column_exclude_list = ['password_hash', 'key']
    form_extra_fields = {
        'password': PasswordField('Password')
    }
    form_args = dict(
        company=dict(
            validators=[DataRequired()]
        ),
        role=dict(
            validators=[DataRequired()]
        )
    )
    form_columns = ['name', 'surname', 'patronymic', 'login', 'email',
                    'password', 'role', 'company', 'bonuses']
    form_excluded_columns = ['password_hash', 'user_login', 'key',
                             'reviewed', 'subjected']
    column_searchable_list = (
        "id", "login", "company.name"
    )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 1


class CompanyModelView(ModelView):
    column_searchable_list = (
        "name",
    )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 1


class CategoryModelView(ModelView):
    column_searchable_list = (
        "name",
    )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 1


class ReviewModelView(ModelView):
    column_searchable_list = (
        "reviewer.id", "company.name",
    )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role_id == 1