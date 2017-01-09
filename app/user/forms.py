import wtforms

# from wtforms import validators
from wtforms.validators import InputRequired
from user.models import User


class LoginForm(wtforms.Form):
    email = wtforms.StringField('Email',  validators=[InputRequired("Please enter your email address.")])
    password = wtforms.PasswordField('Password', validators=[InputRequired("Please enter your password.")])
    remember_me = wtforms.BooleanField('Remember me?', default=True)

    def validate(self):
        if not super(LoginForm, self).validate():
            return False

        self.user = User.authenticate(self.email.data, self.password.data)
        if not self.user:
            self.email.errors.append('Invalid email or password')
            return False
        return True