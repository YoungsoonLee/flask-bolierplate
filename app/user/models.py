import datetime
import re

from app import db, login_manager, bcrypt


@login_manager.user_loader
def _user_loader(user_id):
    return User.query.get(int(user_id))


def slugify(s):
    return re.sub('[^\w]+', '-', s).lower()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(255))
    name = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True)
    active = db.Column(db.Boolean, default=True)
    admin = db.Column(db.Boolean, default=False)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    entries = db.relationship('Entry', backref='author', lazy='dynamic')  # user.author_id  = backref

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<User %r>' % (self.name)

    # flask-login interface
    def get_id(self):
        # return unicode(self.id)
        return str(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_admin(self):
        return self.admin

    @staticmethod
    def make_password(plaintext):
        return bcrypt.generate_password_hash(plaintext)

    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password_hash, raw_password)

    @classmethod
    def create(cls, email, password, **kwargs):
        return User(email=email, password_hash=User.make_password(password), **kwargs)

    @staticmethod
    def authenticate(email, password):
        user = User.query.filter(User.email == email).first()
        if user and user.check_password(password):
            return user
        return False
