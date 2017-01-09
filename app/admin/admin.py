from flask import g, url_for, request, redirect
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from wtforms.fields import SelectField, PasswordField

from app import app, db
from entries.models import Entry, Tag, Comment
from user.models import User


class AdminAuthentication(object):
    def is_accessible(self):
        return g.user.is_authenticated and g.user.is_admin()


class BaseModelView(AdminAuthentication, ModelView):
    pass


class SlugModelView(BaseModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(SlugModelView, self).on_model_change(form, model, is_created)


class EntryModelView(SlugModelView):
    _status_choices = [(choice, label) for choice, label in [
        (Entry.STATUS_PUBLIC, 'Public'),
        (Entry.STATUS_DRAFT, 'Draft'),
        (Entry.STATUS_DELETED, 'Deleted'),
    ]]
    column_choices = {
        'status': _status_choices,
    }
    column_filters = {
        'status', User.name, User.email, 'created_timestamp'
    }
    column_list = ['title', 'status', 'author', 'tease', 'tag_list', 'created_timestamp',]
    column_searchable_list = ['title', 'body']
    column_select_related_list = ['author']

    # for form view
    form_ajax_refs = {
        'author': {
            'fields': (User.name, User.email),  # search on the author's name or e-mail
        }
    }
    form_args = {
        'status': {'choices': _status_choices, 'coerce': int},
    }
    form_columns = ['title', 'body', 'status', 'author', 'tags']
    form_overrides = {'status': SelectField}


class UserModelView(SlugModelView):
    column_filters = ('email', 'name', 'admin', 'active')
    column_list = ['email', 'name', 'admin', 'active',  'created_timestamp']
    column_searchable_list = ['email', 'name']

    form_columns = ['email', 'password', 'name', 'admin', 'active']
    form_extra_fields ={
        'password': PasswordField('New password')
    }

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password_hash = User.make_password(form.password.data)
        return super(UserModelView, self).on_model_change(form, model, is_created)


class BlogFileAdmin(AdminAuthentication, FileAdmin):
    pass


class IndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not (g.user.is_authenticated and g.user.is_admin()):
            return redirect(url_for('login'), next=request.path())
        return self.render('admin/index.html')


admin = Admin(app, 'Blog admin', index_view=IndexView())
# admin.add_view(ModelView(Entry, db.session))
admin.add_view(EntryModelView(Entry, db.session))
admin.add_view(SlugModelView(Tag, db.session))
admin.add_view(UserModelView(User, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(BlogFileAdmin(app.config['STATIC_DIR'], '/static/', name='Static Files'))

