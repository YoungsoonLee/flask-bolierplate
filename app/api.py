from flask.ext.restless import ProcessingException

from app import api
from entries.models import Comment
from entries.forms import CommentForm


def post_preprocessor(data, **kwargs):
    form = CommentForm(data=data)
    if form.validate():
        return form.data
    else:
        raise ProcessingException(
            description='Invalid form submission',
            code=400
        )

api.create_api(
    Comment,
    include_columns=['id', 'name', 'url', 'body', 'created_timestamp'],
    methods=['GET', 'POST'],
    preprocessors={'POST': [post_preprocessor], }
    )
