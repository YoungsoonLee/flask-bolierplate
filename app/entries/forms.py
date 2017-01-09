import wtforms

from entries.models import Entry, Tag
from wtforms import validators
from wtforms.validators import DataRequired, InputRequired


class TagField(wtforms.StringField):

    def _value(self):
        if self.data:
            # Display tags as a comma-seperated list.
            return ', '.join([str(tag.name) for tag in self.data])
        return ''

    def get_tags_from_string(self, tag_string):
        raw_tag = tag_string.split(',')

        # filter out any empty tag names.
        tag_names = [name.strip() for name in raw_tag if name.strip()]

        # Query the database and retrieve any tags we have already saved.
        existing_tags = Tag.query.filter(Tag.name.in_(tag_names))

        # Determine which tag names are new.
        new_names = set(tag_names) - set([str(tag.name) for tag in existing_tags])

        # Create a list of unsaved Tag instances for the new tags
        new_tags = [Tag(name=name) for name in new_names]

        # Return all the existing tags + all the new, unsaved tags.
        return list(existing_tags) + new_tags

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = self.get_tags_from_string(valuelist[0])
        else:
            self.data = []


class EntryForm(wtforms.Form):
    title = wtforms.StringField('Title', validators=[DataRequired()])
    body = wtforms.TextAreaField('Body', validators=[DataRequired()])
    status = wtforms.SelectField('Entry status', choices=(
        (Entry.STATUS_PUBLIC, 'Public'),
        (Entry.STATUS_DRAFT, 'Draft')), coerce=int)
    tags = TagField(
        'Tags',
        description='Separate multiple tags with commas.'
    )

    def save_entry(self, entry):
        self.populate_obj(entry)
        entry.generate_slug()
        return entry


class ImageForm(wtforms.Form):
    file = wtforms.FileField('Image File')


# for comments
class CommentForm(wtforms.Form):
    name = wtforms.StringField('Name', validators=[validators.DataRequired()])
    email = wtforms.StringField('Email',  validators=[validators.DataRequired(),validators.Email()])
    url = wtforms.StringField('URL',  validators=[validators.Optional(), validators.URL()])
    body = wtforms.TextAreaField('Comment',  validators=[validators.DataRequired(), validators.Length(min=10, max=3000)])
    entry_id = wtforms.HiddenField(validators=[validators.DataRequired()])

    def validate(self):
        if not super(CommentForm, self).validate():
            return False

        entry = Entry.query.filter(
            (Entry.status == Entry.STATUS_PUBLIC) &
            (Entry.id == self.entry_id.data)
        ).first()

        if not entry:
            return False

        return True
