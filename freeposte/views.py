import flask_admin as admin
from flask_admin.contrib import sqla

from freeposte import app, db, models

import os

# Flask admin
app_name = os.environ.get('APP_NAME', 'Freeposte.io')
admin = admin.Admin(app, name=app_name, template_mode='bootstrap3')


class BaseModelView(sqla.ModelView):
    pass


class DomainModelView(BaseModelView):
    pass


class UserModelView(BaseModelView):
    pass


class AliasModelView(BaseModelView):
    pass


# Add views
admin.add_view(DomainModelView(models.Domain, db.session))
admin.add_view(UserModelView(models.User, db.session))
admin.add_view(AliasModelView(models.Alias, db.session))
