from freeposte.admin import app, db, models, forms, utils

import os
import pprint
import flask
import flask_login
import json


@app.route('/admin/list', methods=['GET'])
@flask_login.login_required
def admin_list():
    admins = models.User.query.filter_by(global_admin=True)
    return flask.render_template('admin/list.html', admins=admins)


@app.route('/admin/create', methods=['GET', 'POST'])
@flask_login.login_required
def admin_create():
    form = forms.AdminForm()
    form.admin.choices = [
        (user.email, user.email)
        for user in
        flask_login.current_user.get_managed_emails(include_aliases=False)
    ]
    if form.validate_on_submit():
        user = models.User.query.get(form.admin.data)
        if user:
            user.global_admin = True
            db.session.commit()
            flask.flash('User %s is now admin' % user)
            return flask.redirect(flask.url_for('.admin_list'))
        else:
            flask.flash('No such user', 'error')
    return flask.render_template('admin/create.html', form=form)


@app.route('/admin/delete/<admin>', methods=['GET', 'POST'])
@utils.confirmation_required("delete admin {admin }")
@flask_login.login_required
def admin_delete(admin):
    user = models.User.query.get(admin)
    if user:
        user.global_admin  = False
        db.session.commit()
        flask.flash('User %s is no longer admin' % user)
        return flask.redirect(flask.url_for('.admin_list'))
    else:
        flask.flash('No such user', 'error')
    flask.flash('Alias %s deleted' % alias)
    return flask.redirect(
        flask.url_for('.alias_list', domain_name=alias.domain.name))
