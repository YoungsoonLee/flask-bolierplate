import datetime
import re

from user.models import User
from app import db


def slugify(s):
    return re.sub('[^\w]+', '-', s).lower()

entry_tags = db.Table('entry_tags', db.Column('tag_id', db.Integer, db.ForeignKey(
    'tag.id')), db.Column('entry_is', db.Integer, db.ForeignKey('entry.id')))


class Comment(db.Model):
    STATUS_PENDING_MODERATION = 0
    STATUS_PUBLIC = 1
    STATUS_SPAM = 8
    STATUS_DELETED = 9

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    url = db.Column(db.String(100))
    ip_address = db.Column(db.String(64))
    body = db.Column(db.Text)
    status = db.Column(db.SmallInteger, default=STATUS_PUBLIC)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'))

    def __repr__(self):
        return '<Comment from %r>' % (self.name,)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True)

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        # self.slug = slugify(self.name)
        self.generate_slug()

    def generate_slug(self):
        self.slug = ''
        if self.name:
            self.slug = slugify(self.name)

    def __repr__(self):
        return '<Tag: {!r}>'.format(self.name)


class Entry(db.Model):
    STATUS_PUBLIC = 0
    STATUS_DRAFT = 1
    STATUS_DELETED = 2

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text, nullable=False)
    status = db.Column(db.SmallInteger, server_default='0')
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(
        db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tag', secondary=entry_tags,
                           backref=db.backref('entries', lazy='dynamic'))
    comments = db.relationship('Comment', backref='entry', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        # Call parent constructor.
        super(Entry, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        self.slug = ''
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Entry: {!r}>'.format(self.title)

    @property
    def tag_list(self):
        return ', '.join(str(tag.name) for tag in self.tags)

    @property
    def tease(self):
        return self.body[:100]