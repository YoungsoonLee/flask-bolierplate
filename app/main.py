# entry point
from app import app, db

import entries.models
import user.models
import views
import admin.admin
import api

# user
from user.views import user_blueprint
# blog
from entries.views import entries_blueprint

app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(entries_blueprint, url_prefix='/entries')

if __name__ == '__main__':
    app.run()