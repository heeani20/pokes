from flask import render_template, request, redirect, session, url_for, flash, Response
from models import User



#dashboard
def root():
    if 'user_id' not in session:
        return redirect(url_for('users:new_user'))
    return redirect(url_for('dashboard'))

def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('users:new_user'))
    current_user = User.query.get(session['user_id'])
    list_of_all_users = User.query.all()
    count_all_pokes = 0
    for each_post in list_of_all_users:
        count_all_pokes += len(each_post.user_who_poke)

    print(count_all_pokes)

    return render_template('dashboard.html', user=current_user, all_user = list_of_all_users, count_all_pokes=count_all_pokes)

#poke
def poke(id):
    User.add_poke(id)
    print(id)
    return redirect(url_for("dashboard"))


#user
def new_user():
    return render_template("reg_log.html")

def create_user():
    errors = User.register_validation(request.form)
    if errors:
        for error in errors:
            flash(error)
        return redirect(url_for('users:new_user'))
    user_id = User.create(request.form)
    session['user_id'] = user_id
    return redirect(url_for("dashboard"))

def login():
    valid, response = User.login_validation(request.form)
    if not valid:
        flash(response)
        return redirect(url_for("users:new_user"))
    session['user_id'] = response
    return redirect(url_for("dashboard"))

def logout():
    session.clear()
    return redirect(url_for("users:new_user"))
