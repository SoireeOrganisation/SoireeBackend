from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import PasswordField, SelectField
from wtforms.validators import DataRequired

from .models import update_session


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

    def update_model(self, form, model):
        """
            Update model from form.
            :param form:
                Form instance
            :param model:
                Model instance
        """
        try:
            form.populate_obj(model)
            self._on_model_change(form, model, False)
            update_session(model)
        except Exception as ex:
            if not self.handle_view_exception(ex):
                print('Failed to update record.')

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, False)

        return True


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