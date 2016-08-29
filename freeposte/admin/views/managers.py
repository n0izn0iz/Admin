from freeposte.admin import app, db, models, forms, access

import flask
import flask_login


@app.route('/manager/list/<domain_name>', methods=['GET'])
@access.domain_admin(models.Domain, 'domain_name')
def manager_list(domain_name):
    domain = models.Domain.query.get(domain_name) or flask.abort(404)
    return flask.render_template('manager/list.html', domain=domain)


@app.route('/manager/create/<domain_name>', methods=['GET', 'POST'])
@access.domain_admin(models.Domain, 'domain_name')
def manager_create(domain_name):
    domain = models.Domain.query.get(domain_name) or flask.abort(404)
    form = forms.ManagerForm()
    available_users = flask_login.current_user.get_managed_emails(
        include_aliases=False)
    form.manager.choices = [
        (user.email, user.email) for user in available_users
    ]
    if form.validate_on_submit():
        user = models.User.query.get(form.manager.data)
        if user not in available_users:
            flask.abort(403)
        elif user in domain.managers:
            flask.flash('User %s is already manager' % user, 'error')
        else:
            domain.managers.append(user)
            db.session.commit()
            flask.flash('User %s can now manage %s' % (user, domain.name))
            return flask.redirect(
                flask.url_for('.manager_list', domain_name=domain.name))
    return flask.render_template('manager/create.html',
        domain=domain, form=form)


# TODO For now the deletion behaviour is broken and reserved to
# global admins.
@app.route('/manager/delete/<manager>', methods=['GET', 'POST'])
@access.confirmation_required("remove manager {manager}")
@access.global_admin
def manager_delete(manager):
    user = models.User.query.get(manager)
    if user in user.domain.managers:
        user.domain.managers.remove(user)
        db.session.commit()
        flask.flash('User %s can no longer manager %s' % (user, user.domain))
    else:
        flask.flash('User %s is not manager' % user, 'error')
    return flask.redirect(
        flask.url_for('.manager_list', domain_name=user.domain.name))
